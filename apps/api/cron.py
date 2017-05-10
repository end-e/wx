# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/19 14:04'
import datetime

from django.db import connection as conn
from django.core.cache import caches
from wechatpy import WeChatClient

from .models import AccessToken, Log
from utils import db, consts


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
    try:
        orders = get_user_order()
        wechat_users = get_wechat_users(orders)
        for wechat_user in wechat_users:
            userId = wechat_user['membernumber']
            for order in orders:
                if order['CardNo'].strip() == userId:
                    openid = wechat_user['openid']
                    data = {}
                    # 模版数据字典
                    data['message'] = {
                        "value": str(float('%.2f' % order['PayMoney'])),
                        "color": "#173177"
                    }
                    data['message2'] = {
                        "value": wechat_user['username'],
                        "color": "#173177"
                    }
                    send_temp(openid, data)
    except Exception as e:
        pass


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

    sql = "SELECT a.PurchSerial, a.PayMoney,a.CardNo,a.PurchDateTime,a.shopID,a.Point " \
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
    users = "'" + "','".join(users) + "'"
    sql_sel_wechat = "SELECT openid,username,membernumber FROM wechat_user WHERE membernumber IN ({users})" \
        .format(users=users)

    conn2 = db.getMysqlConn()
    cur = conn2.cursor()
    cur.execute(sql_sel_wechat)
    wechat_users = cur.fetchall()
    cur.close()
    conn.close()

    return wechat_users


def send_temp(openid, data):
    app_id = consts.APPID
    secret = consts.APPSECRET

    # 用户openid
    # oE9Pts9_cBLTWccP682FgWuvQ7js
    # oE9Pts_Hk63sj3dlmCtfkXGWMV-8
    user_id = 'oE9Pts9_cBLTWccP682FgWuvQ7js'
    access_token = caches['default'].get('wx_access_token', '')
    if not access_token:
        access_token = cron_get_token()

    client = WeChatClient(app_id, secret, access_token)
    message = client.message
    # 模版id
    template_id = '0twv952J80MHBUm_WUQfgNPG9w7_FyALpYxSpAvgVjc'
    url = ''
    top_color = '#efefef'
    miniprogram = {}
    data = data

    res_send = message.send_template(user_id, template_id, url, top_color, data)

    Log.objects.create(
        access_token=access_token,
        open_id=data['message2']['value'],
        errmsg=res_send['errmsg'],
        errcode=res_send['errcode'],
        last_purchserial=caches['default'].get('last_purchserial', ''),
        type='02',
    )
    if res_send['errmsg'] != 'ok':
        # TODO:记录发送失败日志
        pass
