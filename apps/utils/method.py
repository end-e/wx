import random,hashlib,datetime,json,requests,time,threading

from django.core.cache import caches
from django.db import transaction
from wechatpy import WeChatClient

from user.models import WechatMembers
from api.models import LogWx
from utils import db,consts
from admin.models import GiftOrder,GiftOrderInfo,GiftCardCode,ShopOrder,GiftBalanceChangeLog

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
    shopDict = caches['default'].get('base_shopDict', '')
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

        conn2 = db.getMysqlConnection(
            consts.DB_SERVER_18,
            consts.DB_PORT_18,
            consts.DB_USER_18,
            consts.DB_PASSWORD_18,
            'kgscm_ts'
        )
        sql2 = "SELECT Shopcode,Shopnm FROM bas_shop WHERE enable = 1"
        cur2 = conn2.cursor()
        cur2.execute(sql2)
        shops2 = cur.fetchall()

        shops = shops + shops2

        shopDict = {shop['Shopcode']: shop['Shopnm'].strip() for shop in shops}
        caches['default'].set('base_shopDict', shopDict, 60 * 60 * 12)

    return shopDict.get(id,id)



def get_ip(request):
    """
    获取ip
    :param request:
    :return:
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
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
        md5.update(data.encode(encoding='utf-8'))
    return md5.hexdigest()


def get_access_token(app_name, app_id, secret):
    client = WeChatClient(app_id, secret)
    response = client.fetch_access_token()
    token = response['access_token']
    key = 'wx_{app_name}_access_token'.format(app_name=app_name)
    caches['default'].set(key, token, 7200)

    return token


def getTimeStamp(str):
    time.strptime(str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(time.strptime(str, '%Y-%m-%d %H:%M:%S'))


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

    return orders


def get_wechat_users(orders):
    users = [order['CardNo'].strip() for order in orders]
    wechat_users = WechatMembers.objects.values('openid', 'username', 'membernumber').filter(membernumber__in=users)

    return wechat_users


def create_temp_data(order):
    data = {}
    # 模版数据字典
    data['first'] = {
        "value": "宽广会员专享优惠券-爱宽广微信小程序",
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


def send_temp(msg):
    # 用户openid
    user_id = msg['openid']
    app_id = msg['app_id']
    secret = msg['secret']
    access_token = msg['access_token']
    data = msg['data']

    client = WeChatClient(app_id, secret, access_token)
    message = client.message
    # 模版id
    template_id = 'eddBYOpWHXKIiZ0IW74uUrDGUyBwjgjwSq1C5s-j_uo'

    mini_program = {
        'appid': consts.WX_APP_ID,
        'pagepath': 'pages/index/index'
    }
    res_send = message.send_template(user_id, template_id, data, None, mini_program)

    if res_send['errmsg'] != 'ok':
        LogWx.objects.create(
            type='1',
            remark='openid:' + user_id,
            errmsg=res_send['errmsg'],
            errcode=res_send['errcode']
        )



def gift_compare_order(offset=0):
    res = {}
    res['status'] = 0
    res_get = gift_get_Wx_order(offset)
    if res_get['status'] == 0:
        offset = res_get['offset']
        total_count = res_get['total_count']
        wx_orders = res_get['wx_orders']
        gift_save_local_order(wx_orders)

        if total_count > (offset + 1) * 100:
            gift_compare_order(offset + 1)

    else:
        res['status'] = 1

    return res


def gift_get_Wx_order(offset=0):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    url = "https://api.weixin.qq.com/card/giftcard/order/batchget?access_token={access_token}" \
        .format(access_token=access_token)
    today = datetime.date.today().strftime('%Y-%m-%d')
    begin_time = getTimeStamp(today + ' 00:00:00')
    end_time = getTimeStamp(today + ' 23:59:59')
    data = {
        "begin_time": begin_time,
        "end_time": end_time,
        "sort_type": "DESC",
        "offset": offset,
        "count": 100
    }
    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    rep = requests.post(url, data=data)
    rep_data = json.loads(rep.text)
    res = {}
    if rep_data['errmsg'] == 'ok':
        total_count = rep_data['total_count']
        wx_orders = rep_data['order_list']
        res['status'] = 0
        res['offset'] = offset
        res['total_count'] = total_count
        res['wx_orders'] = wx_orders
    else:
        res['status'] = 1
        LogWx.objects.create(type='6', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
                             remark='cron_giftcard_wx_local')

    return res


def gift_save_local_order(wx_orders):
    for order in wx_orders:
        order_qs = GiftOrder.objects.filter(order_id=order['order_id'])
        if not order_qs:
            try:
                with transaction.atomic():
                    order_save = GiftOrder.objects.create(
                        order_id=order['order_id'], trans_id=order['trans_id'],
                        create_time=order['create_time'], pay_finish_time=order['pay_finish_time'],
                        total_price=order['total_price'], open_id=order['open_id']
                    )
                    orderID = order_save.id
                    info_list = []
                    code_list = []
                    for card in order['card_list']:
                        code_list.append(card['code'])
                        info = GiftOrderInfo()
                        info.order_id = orderID
                        info.card_id = card['card_id']
                        info.price = card['price']
                        info.code = card['code']
                        info_list.append(info)
                    GiftOrderInfo.objects.bulk_create(info_list)
                    GiftCardCode.objects.filter(code__in=code_list).update(status='1')
            except Exception as e:
                print(e)
                LogWx.objects.create(
                    type='6',
                    errmsg=e,
                    errcode='6',
                    remark='wx_order_id:{order}'.format(order=order['order_id'])
                )


def createOrderSn(objModel):
    today = datetime.datetime.today()
    begin = today.strftime('%Y-%m-%d') + ' 00:00:00'
    end = today.strftime('%Y-%m-%d') + ' 23:59:59'

    count = objModel.objects.filter(save_time__lte=end, save_time__gte=begin).count()
    sn = str(count + 1).zfill(4)
    sn = today.strftime('%Y%m%d') + sn

    return sn


def getGiftBalance():
    conn_226 = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    balanceChangeLog = GiftBalanceChangeLog.objects.values('last_serial').first()
    prev_last_serial = ''
    if balanceChangeLog:
        prev_last_serial = balanceChangeLog['last_serial']
        whereStr = "a.PurchSerial> '{last_serial}'".format(last_serial=prev_last_serial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    # sql_order = "SELECT a.detail, a.CardNo,a.PurchSerial FROM GuestPurch0 AS a,guest AS b " \
    #             "WHERE " + whereStr + " AND a.CardNo=b.CardNo AND b.cardtype = 12 ORDER BY a.PurchSerial "

    sql_order = " SELECT a.detail, a.CardNo,a.PurchSerial" \
                " FROM GuestPurch0 as a LEFT JOIN guest AS b ON a.CardNo=b.CardNo" \
                " WHERE " + whereStr + " AND b.cardtype = 12" \
                " ORDER BY a.PurchSerial"
    cur_226 = conn_226.cursor()
    cur_226.execute(sql_order)
    orders = cur_226.fetchall()

    cardNo_list = [int(order['CardNo']) for order in orders]

    log_list = LogWx.objects.values('id','remark','repeat_status').filter(type='2',errcode__in=['40001','40073','-1'],repeat_status='0')

    for log in log_list:
        item = {}
        remark_list = log['remark'].split(',')
        for remark in remark_list:
            r = remark.split(':')
            item[r[0]] = r[1]
        if int(item['CardNo']) not in cardNo_list:
            item['id'] = log['id']
            item['repeat_status'] = log['repeat_status']
            orders.append(item)

    orders = sorted(orders,key= lambda order:int(order['PurchSerial']))

    return prev_last_serial,orders


def getGuestPoint(member_id):
    conn = db.getMsSqlConn()
    sql = "SELECT Point FROM guest as a,cardType as b WHERE cardNO='{cardNO}' AND b.flag='0'".format(cardNO=member_id)
    cur = conn.cursor()
    cur.execute(sql)
    guest = cur.fetchone()
    point = 0
    if guest:
        point = float(guest['Point'])
    return point


def updateGuestPoint(member_id,total_pay):
    conn = db.getMsSqlConn()
    cur = conn.cursor()
    res = True
    try:
        conn.autocommit(False)
        sql =  "UPDATE guest SET Point = Point-{total_pay} WHERE cardNO='{cardNO}'"\
            .format(cardNO=member_id,total_pay=total_pay)
        cur.execute(sql)
        if cur.rowcount == 1:
            conn.commit()
        else:
            res = False
    except Exception as e:
        print(e)
        conn.rollback()
        res = False

    return res
