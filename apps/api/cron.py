# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/4/19 14:04'
from django.db import connection as conn
from django.http import HttpResponse
from wechatpy import WeChatClient

import datetime,json

from .models import AccessToken,Log
from utils import db, consts


def crontab_get_token():
    AccessToken.objects.create(
        add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        access_token='my_scheduled_job',
        expires_in='7200',
    )
    return HttpResponse('my_scheduled_job')


def cron_send_temp():
    orders = get_user_order()
    wechat_users = get_wechat_users(orders)
    for wechat_user in wechat_users:
        userId = wechat_user['membernumber']
        for order in orders:
            if order['CardNo'].strip() == userId:
                openid = wechat_user['openid']
                data = {}
                data['first'] = {
                    "value": float(order['PayMoney']),
                    "color": "#173177"
                }
                data['key1'] = {
                    "value": wechat_user['username'],
                    "color": "#173177"
                }
                send_temp(openid,data)


def get_user_order():
    # TODO：查询ERP内的消费数据
    conn = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    sql = "SELECT a.PayMoney,a.CardNo,a.PurchDateTime,a.shopID,a.Point FROM GuestPurch0 AS a,guest AS b,cardtype AS c " \
          " WHERE PurchDateTime> '{start}' AND a.cardno=b.cardno AND  b.cardtype = c.cardtype AND  c.flag = 0" \
        .format(start=start)

    cur = conn.cursor()
    cur.execute(sql)
    orders = cur.fetchall()
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


def send_temp(openid,data):
    app_id = 'wxd892ee844883f6a8'
    secret = '8888eb81688a37912e05ba0520ac4b70'
    client = WeChatClient(app_id, secret)

    message = client.message
    #用户openid
    user_id = 'ouCqqv7gRJtLb6oUwCvG0QdeJ6Ec'
    #模版id
    template_id = 'LgOhnBWTPdJ2sjjTuCjePq2tdqp2YYWqQlwdIyyh0zE'
    url = ''
    top_color = '#efefef'
    miniprogram = {}
    data = data

    res_send = message.send_template(user_id, template_id, url, top_color, data)
    Log.objects.create(
        errmsg = res_send['errmsg'],
        errcode = res_send['errcode'],
        type = '02',
    )
    if res_send['errmsg'] != 'ok':
        #TODO:记录发送失败日志
        pass

