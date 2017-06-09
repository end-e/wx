# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/19 14:04'
import datetime

from django.core.cache import caches
from wechatpy import WeChatClient

from api.models import AccessToken, Log
from user.models import WechatMembers
from utils import db, consts,method


def cron_get_token():
    app_id = consts.APPID
    secret = consts.APPSECRET
    client = WeChatClient(app_id, secret)
    response = client.fetch_access_token()
    token = response['access_token']
    caches['default'].set('wx_access_token', token, 7200)
    # 测试access_token为什么会超出上限
    access_token = AccessToken()
    access_token.access_token = token
    access_token.expires_in = response['expires_in']
    access_token.save()
    return token


def cron_send_temp():
    orders = get_user_order()
    wechat_users = get_wechat_users(orders)
    for wechat_user in wechat_users:
        userId = wechat_user['membernumber']
        for order in orders:
            if order['CardNo'].strip() == userId:
                openid = wechat_user['openid']
                data = create_temp_data(order)

                send_temp(openid, data)


def get_user_order():
    # TODO：查询ERP内的消费数据
    conn = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    last_purchserial = caches['default'].get('last_purchserial', '')
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
        caches['default'].set('last_purchserial', last_one, 2 * 60)
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
        "value": method.getShopName(order['shopID']) + "(" + order['Branchno'] + "/" + str(order['ListNO']) + ")",
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
    # oE9Pts9_cBLTWccP682FgWuvQ7js
    # oE9Pts_Hk63sj3dlmCtfkXGWMV-8
    user_id = openid
    access_token = caches['default'].get('wx_access_token', '')
    if not access_token:
        access_token = cron_get_token()

    client = WeChatClient(app_id, secret, access_token)
    message = client.message
    # 模版id
    template_id = 'eddBYOpWHXKIiZ0IW74uUrDGUyBwjgjwSq1C5s-j_uo'
    url = ''
    top_color = '#efefef'
    data = data

    res_send = message.send_template(user_id, template_id, url, top_color, data)

    Log.objects.create(
        access_token=access_token,
        open_id=openid,
        errmsg=res_send['errmsg'],
        errcode=res_send['errcode'],
        last_purchserial=caches['default'].get('last_purchserial', ''),
        type='02',
    )
    if res_send['errmsg'] != 'ok':
        # TODO:记录发送失败日志
        pass
