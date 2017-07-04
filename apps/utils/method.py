import random,hashlib,datetime

from django.core.cache import caches
from wechatpy import WeChatClient
from user.models import WechatMembers
from api.models import LogWx

from utils import db,consts

def createNonceStr(length = 16):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    str = ""
    for i in range(0,length):
        _index = random.randint(0, len(chars) - 1)
        str += chars[_index:_index+1]
    return str


def getShopName(id):
    """
    门店code==》门店名称
    :param id:
    :return:
    """
    shopDict = caches['default'].get('base_shopDict','')
    if not shopDict:
        conn = db.getMysqlConnection(
            consts.DB_SERVER_18,
            consts.DB_PORT_18,
            consts.DB_USER_18,
            consts.DB_PASSWORD_18,
            consts.DB_DATABASE_18
        )
        sql = "SELECT Shopcode,Shopnm FROM bas_shop WHERE enable = 1"
        cur = conn.cursor()
        cur.execute(sql)
        shops = cur.fetchall()
        shopDict = {shop['Shopcode']:shop['Shopnm'].strip() for shop in shops}
        caches['default'].set('base_shopDict', shopDict,60*60*12)

    return shopDict[id]


def get_ip(request):
    """
    获取ip
    :param request:
    :return:
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def md5(data):
    """
    md5加密
    :param data:
    :return:
    """
    md5 = hashlib.md5()
    if data:
        md5.update(data.encode(encoding = 'utf-8'))
    return md5.hexdigest()


def get_access_token(app_name,app_id,secret):
    client = WeChatClient(app_id, secret)
    response = client.fetch_access_token()
    token = response['access_token']
    key = 'wx_{app_name}_access_token'.format(app_name=app_name)
    caches['default'].set(key, token, 7200)

    return token


def get_user_order():
    # TODO：查询ERP内的消费数据
    conn = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    last_purchserial = caches['default'].get('wx_ikg_tempmsg_last_purchserial', '')
    if last_purchserial:
        whereStr = "a.PurchSerial> '{last_purchserial}'".format(last_purchserial=last_purchserial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    sql = "SELECT a.PurchSerial, a.PayMoney,a.CardNo,a.PurchDateTime,a.shopID,a.Point,a.HistoryPoint,a.ListNO,a.Branchno " \
          "FROM GuestPurch0 AS a,guest AS b,cardtype AS c " \
          "WHERE " + whereStr + " AND a.cardno=b.cardno AND  b.cardtype = c.cardtype AND  c.flag = 0 " \
                                "ORDER BY a.PurchSerial"

    cur = conn.cursor()
    cur.execute(sql)
    orders = cur.fetchall()
    if len(orders) > 0:
        last_one = orders[-1]['PurchSerial']
        caches['default'].set('wx_ikg_tempmsg_last_purchserial', last_one, 7 * 24 * 60 * 60)
    cur.close()
    conn.close()

    return orders


def get_wechat_users(orders):
    users = [order['CardNo'].strip() for order in orders]
    wechat_users = WechatMembers.objects.values('openid','username','membernumber').filter(membernumber__in=users)

    return wechat_users


def create_temp_data(order):
    data = {}
    # 模版数据字典
    data['first'] = {
        "value": "宽广超市会员",
        "color": "#173177"
    }
    data['keyword1'] = {
        "value": order['CardNo'].strip(),
        "color": "#173177"
    }
    data['keyword2'] = {
        "value": getShopName(order['shopID']) + "(" + order['Branchno'] + "/" + str(order['ListNO']) + ")",
        "color": "#173177"
    }
    data['keyword3'] = {
        "value": str(float('%.2f' % order['PayMoney'])),
        "color": "#173177"
    }
    data['remark'] = {
        "value": "消费日期：" + order['PurchDateTime'].strftime("%Y-%m-%d %H:%M:%S") + ' \n详询4001110314',
        "color": "#173177"
    }

    return data


def send_temp(openid, data):
    app_id = consts.APPID
    secret = consts.APPSECRET

    # 用户openid
    user_id = openid
    access_token = caches['default'].get('wx_ikg_access_token', '')
    if not access_token:
        access_token = get_access_token('ikg',app_id,secret)
    client = WeChatClient(app_id, secret, access_token)
    message = client.message
    # 模版id
    template_id = 'eddBYOpWHXKIiZ0IW74uUrDGUyBwjgjwSq1C5s-j_uo'
    url = ''
    top_color = '#efefef'
    data = data
    res_send = message.send_template(user_id, template_id, url, top_color, data)

    if res_send['errmsg'] != 'ok':
        # TODO:记录发送失败日志
        LogWx.objects.create(
            type='1',
            remark='openid:'+openid,
            errmsg=res_send['errmsg'],
            errcode=res_send['errcode']
        )