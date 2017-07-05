# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/19 14:04'
import datetime,json,requests

from django.core.cache import caches

from admin.models import GiftCardCode, GiftBalanceChangeLog
from api.models import LogWx
from utils import db, consts,method


def cron_get_ikg_token():
    '''
    获取并缓存 爱宽广access_token
    :return: access_token
    '''
    app_id = consts.APPID
    secret = consts.APPSECRET
    method.get_access_token( 'ikg',app_id, secret,)


def cron_get_kgcs_token():
    """
    获取并缓存 宽广超市access_token
    :return: access_token
    """
    app_id = consts.KG_APPID
    secret = consts.KG_APPSECRET
    method.get_access_token('kgcs',app_id, secret)


def cron_send_temp():
    orders = method.get_user_order()
    wechat_users = method.get_wechat_users(orders)
    for wechat_user in wechat_users:
        userId = wechat_user['membernumber']
        for order in orders:
            if order['CardNo'].strip() == userId:
                openid = wechat_user['openid']
                data = method.create_temp_data(order)

                method.send_temp(openid, data)


def cron_giftcard_balance_change():
    # 1、查询消费记录
    # conn_226 = db.getMsSqlConn()
    conn_226 = db.getMsSqlConn22()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    balanceChangeLog = GiftBalanceChangeLog.objects.values('last_serial').first()
    prev_last_serial = ''
    if balanceChangeLog:
        prev_last_serial = balanceChangeLog['last_serial']
        whereStr = "a.PurchSerial> '{last_serial}'".format(last_serial=prev_last_serial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    sql_order = "SELECT a.detail, a.CardNo,a.PurchSerial " \
                "FROM GuestPurch0 AS a,guest AS b, (SELECT cardno, MAX (purchserial) PurchSerial from GuestPurch0 GROUP BY cardno) AS c " \
                "WHERE " + whereStr + " AND a.CardNo=b.CardNo AND b.cardtype = 12 AND a.PurchSerial=c.PurchSerial ORDER BY a.PurchSerial "
    cur_226 = conn_226.cursor()
    cur_226.execute(sql_order)
    orders = cur_226.fetchall()
    if len(orders) > 0:
        try:
            # 2、拼接wx_card_id
            for order in orders:
                qs_card = GiftCardCode.objects.values('wx_card_id').filter(code=order['CardNo']).first()
                order['wx_card_id'] = qs_card['wx_card_id']

            access_token = caches['default'].get('wx_kgcs_access_token', '')
            if not access_token:
                method.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

            for o in orders:
                url = 'https://api.weixin.qq.com/card/generalcard/updateuser?access_token={token}' \
                    .format(token=access_token)
                data = {
                    "code": o['CardNo'].strip(),
                    "card_id": o['wx_card_id'],
                    "balance": float(o['detail'])
                }

                data = json.dumps(data, ensure_ascii=False).encode('utf-8')
                rep = requests.post(url, data=data)
                rep_data = json.loads(rep.text)
                if rep_data['errcode'] != 0:
                    # TODO 记录错误日志
                    LogWx.objects.create(
                        type='2',
                        remark='code:{code},balance:{balance},card_id:{card_id}'.format(code=o['CardNo'].strip(),balance=str(float(o['detail'])),card_id=o['wx_card_id']),
                        errmsg=rep_data['errmsg'],
                        errcode=rep_data['errcode']
                    )

            this_last_serial = orders[-1]['PurchSerial']
            if prev_last_serial:
                GiftBalanceChangeLog.objects.update(last_serial=this_last_serial) \
                    .filter(last_serial=prev_last_serial, create_time=datetime.datetime.now)
            else:
                GiftBalanceChangeLog.objects.create(last_serial=this_last_serial)
        except Exception as e:
            LogWx.objects.create(
                type='0',
                errmsg=e,
                errcode='0'
            )
