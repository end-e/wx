# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/19 14:04'
import datetime, time,requests,json
from threading import Thread

from django.core.cache import caches
from django.http import HttpResponse

from admin.models import GiftCardCode, GiftBalanceChangeLog
from api.models import LogWx
from utils import db, consts, method


def cron_get_ikg_token(req):
    '''
    获取并缓存 爱宽广access_token
    :return: access_token
    '''
    app_id = consts.APPID
    secret = consts.APPSECRET
    method.get_access_token('ikg', app_id, secret, )


def cron_get_kgcs_token():
    """
    获取并缓存 宽广超市access_token
    :return: access_token
    """
    app_id = consts.KG_APPID
    secret = consts.KG_APPSECRET
    method.get_access_token('kgcs', app_id, secret)


def cron_send_temp():
    orders = method.get_user_order()
    if len(orders)>0:
        wechat_users = method.get_wechat_users(orders)
        for wechat_user in wechat_users:
            userId = wechat_user['membernumber']
            for order in orders:
                if order['CardNo'].strip() == userId:
                    openid = wechat_user['openid']
                    data = method.create_temp_data(order)
                    t = Thread(target=method.send_temp,args=(openid, data))
                    t.start()


def cron_gift_change_balance():
    # 1、查询消费记录
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

    sql_order = "SELECT a.detail, a.CardNo,a.PurchSerial FROM GuestPurch0 AS a,guest AS b " \
                "WHERE " + whereStr + " AND a.CardNo=b.CardNo AND b.cardtype = 12 ORDER BY a.PurchSerial "
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

            threads = []
            for o in orders:
                thread = Thread(target=gift_change_balance,args=(o['CardNo'].strip(),o['wx_card_id'],o['detail'],access_token))
                threads.append(thread)
                thread.start()
                # gift_change_balance(o, access_token)

            this_last_serial = orders[-1]['PurchSerial']

            if prev_last_serial:
                now = datetime.datetime.now()
                GiftBalanceChangeLog.objects.filter(last_serial=prev_last_serial) \
                    .update(last_serial=this_last_serial,create_time=now.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                GiftBalanceChangeLog.objects.create(last_serial=this_last_serial)
            res_msg = 'ok'
        except Exception as e:
            print(e)
            LogWx.objects.create(type='2', errmsg=e, errcode='2')
            res_msg = e
    else:
        res_msg = 'no order'

    return HttpResponse(res_msg)


def cron_gift_change_balance2():
    prev_id = caches['default'].get('wx_log_balance_id', '')

    kwarg = {}
    if prev_id:
        kwarg.setdefault('id__gt',prev_id)
    kwarg.setdefault('type', 2)
    kwarg.setdefault('errcode', 40001)
    log_list = LogWx.objects.values('id','remark').filter(**kwarg)
    LogWx.objects.create(type='2', errmsg=len(log_list), errcode='2')
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        method.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)
    if(len(log_list)>0):
        try:
            threads = []
            for log in log_list:
                remark = log['remark']
                info = remark.split(',')
                info = {obj.split(':')[0]: obj.split(':')[1] for obj in info }

                thread = Thread(target=gift_change_balance, args=(info['card_id'].strip(), info['code'], info['balance'], access_token))
                threads.append(thread)
                thread.start()
            last_id = log_list[-1]['id']
            caches['default'].set('wx_log_balance_id', last_id)
            res_msg = 'ok'
        except Exception as e:
            print(e)
            LogWx.objects.create(type='2', errmsg=e, errcode='2')
            res_msg = e

    else:
        res_msg = 'no order'

    return HttpResponse(res_msg)

def gift_change_balance(card_id,code,balance,access_token):
    url = 'https://api.weixin.qq.com/card/generalcard/updateuser?access_token={token}' \
        .format(token=access_token)
    data = {
        "code": code,
        "card_id": card_id,
        "balance": float(balance) * 100
    }

    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    rep = requests.post(url, data=data, headers={'Connection': 'close'})
    rep_data = json.loads(rep.text)
    if rep_data['errcode'] != 0:
        # TODO 记录错误日志
        LogWx.objects.create(
            type='2', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
            remark='code:{code},balance:{balance},card_id:{card_id}'
                .format(code=o['CardNo'].strip(), balance=str(float(o['detail'])),
                        card_id=card_id)
        )


def cron_gift_compare_order():
    res = method.gift_compare_order()
    if res['status'] == 1:
        LogWx.objects.create(type='0', errmsg='cron_gift_compare_order_fail', errcode='0')
        return HttpResponse('fail')
    return HttpResponse('ok')



