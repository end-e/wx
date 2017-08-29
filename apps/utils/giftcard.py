# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:24'
import datetime,json,requests

from django.core.cache import caches

from api.models import LogWx
from utils import wx,consts,method,data

def gift_compare_order(offset=0):
    res = {}
    res['status'] = 0
    res_get = get_Wx_order(offset)
    if res_get['status'] == 0:
        offset = res_get['offset']
        total_count = res_get['total_count']
        wx_orders = res_get['wx_orders']
        data.local_save_gift_order(wx_orders)
        if total_count > (offset + 1) * 100:
            gift_compare_order(offset + 1)

    else:
        res['status'] = 1

    return res


def get_Wx_order(offset=0):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        wx.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    url = "https://api.weixin.qq.com/card/giftcard/order/batchget?access_token={access_token}" \
        .format(access_token=access_token)
    today = datetime.date.today().strftime('%Y-%m-%d')
    begin_time = method.getTimeStamp(today + ' 00:00:00')
    end_time = method.getTimeStamp(today + ' 23:59:59')
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


def change_balance(order,access_token):
    try:
        code = order['CardNo'].strip()
        card_id = order['wx_card_id']
        balance= float(order['detail'])
        serial= order['PurchSerial']
        url = 'https://api.weixin.qq.com/card/generalcard/updateuser?access_token={token}' \
            .format(token=access_token)
        data = {
            "code": code,
            "card_id": card_id,
            "balance": balance * 100
        }

        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        rep = requests.post(url, data=data, headers={'Connection': 'close'})
        rep_data = json.loads(rep.text)
        if 'repeat_status' in order and rep_data['errcode'] == 0 :
            LogWx.objects.filter(id=order['id']).update(repeat_status='1')

        log = LogWx()
        log.type = 2
        log.errmsg = rep_data['errmsg']
        log.errcode = rep_data['errcode']
        log.remark = 'PurchSerial:{serial},CardNo:{code},detail:{balance},card_id:{card_id}'\
            .format(serial=serial, code=code, balance=str(float(balance)), card_id=card_id)
        if rep_data['errcode'] != 0:
            log.repeat_status = '0'
        log.save()
    except Exception as e:
        print(e)
        LogWx.objects.create(type='2', errmsg=e, errcode='2')




