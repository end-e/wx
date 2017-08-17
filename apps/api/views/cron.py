# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/19 14:04'
import datetime, time,requests,json
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import caches
from django.http import HttpResponse

from admin.models import GiftCardCode, GiftBalanceChangeLog
from api.models import LogWx
from utils import db, consts, method


def cron_get_ikg_token():
    '''
    获取并缓存 爱宽广access_token
    :return: access_token
    '''
    app_id = consts.APPID
    secret = consts.APPSECRET
    token = method.get_access_token('ikg', app_id, secret, )
    return HttpResponse(token)


def cron_get_kgcs_token():
    """
    获取并缓存 宽广超市access_token
    :return: access_token
    """
    app_id = consts.KG_APPID
    secret = consts.KG_APPSECRET
    token = method.get_access_token('kgcs', app_id, secret)
    return HttpResponse(token)


def cron_send_temp():
    app_id = consts.APPID
    secret = consts.APPSECRET
    access_token = caches['default'].get('wx_ikg_access_token', '')
    if not access_token:
        access_token = method.get_access_token('ikg', app_id, secret)

    orders = method.get_user_order()
    if len(orders)>0:
        wechat_users = method.get_wechat_users(orders)
        try:
            threads = []
            msg_list = []

            for wechat_user in wechat_users:
                userId = wechat_user['membernumber']
                for order in orders:
                    if order['CardNo'].strip() == userId:
                        openid = wechat_user['openid']
                        data = method.create_temp_data(order)
                        msg ={
                            'openid':openid,
                            'data':data,
                            'app_id':app_id,
                            'secret':secret,
                            'access_token':access_token
                        }
                        # msg_list.append(msg)
                        thread = Thread(target=method.send_temp,args=(msg,))
                        threads.append(thread)
                        thread.start()
            for t in threads:
                t.join()
            # if len(msg_list)>0:
            #     pool = ThreadPoolExecutor(len(msg_list)+1)
            #     for msg in msg_list:
            #         pool.submit(method.send_temp,msg)
        finally:
            last_one = orders[-1]['PurchSerial']
            caches['default'].set('wx_ikg_tempmsg_last_purchserial', last_one, 7 * 24 * 60 * 60)


def cron_gift_change_balance():
    # 1、查询消费记录

    prev_last_serial, orders = method.getGiftBalance()
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
                thread = Thread(target=gift_change_balance,args=(o['wx_card_id'],o['CardNo'].strip(),o['detail'],access_token,))
                threads.append(thread)
                thread.start()
            for t in threads:
                t.join()

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

                thread = Thread(target=gift_change_balance,
                                args=(info['card_id'].strip(), info['code'], info['balance'], access_token,)
                                )
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
    res = {'status':0}
    LogWx.objects.create(
        type='2', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
        remark='code:{code},balance:{balance},card_id:{card_id}'
            .format(code=code, balance=str(float(balance)), card_id=card_id)
    )
    if rep_data['errcode'] != 0:
        # TODO 记录错误日志
        LogWx.objects.create(
            type='2', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
            remark='code:{code},balance:{balance},card_id:{card_id}'
            .format(code=code, balance=str(float(balance)),card_id=card_id)
        )
        res['status'] = 1


def cron_gift_compare_order():
    res = method.gift_compare_order()
    if res['status'] == 1:
        LogWx.objects.create(type='0', errmsg='cron_gift_compare_order_fail', errcode='0')
        return HttpResponse('fail')
    return HttpResponse('ok')



