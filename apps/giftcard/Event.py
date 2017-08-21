# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/5 17:40'
import json,requests

from django.db import transaction

from admin.models import GiftCardCode,GiftOrder,GiftOrderInfo
from api.models import LogWx
from django.core.cache import caches
from utils import method,consts


def giftcard_pay_done(order_id):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        method.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    url = 'https://api.weixin.qq.com/card/giftcard/order/get?access_token={token}' \
        .format(token=access_token)
    data = {"order_id": order_id}
    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    client = requests.Session()
    rep = client.post(url, data=data, headers={'Connection': 'close'})
    rep_data = json.loads(rep.text)

    res = {}
    if rep_data['errcode'] == 0:
        order = rep_data['order']
        card_list = order['card_list']
        try:
            with transaction.atomic():
                order = GiftOrder.objects.create(
                    order_id=order['order_id'], trans_id=order['trans_id'],
                    create_time=order['create_time'], pay_finish_time=order['pay_finish_time'],
                    total_price=order['total_price'], open_id=order['open_id']
                )
                orderID = order.id
                info_list = []
                code_list = []
                for card in card_list:
                    code_list.append(card['code'])
                    info = GiftOrderInfo()
                    info.order_id = orderID
                    info.card_id = card['card_id']
                    info.price = card['price']
                    info.code = card['code']
                    info_list.append(info)
                GiftOrderInfo.objects.bulk_create(info_list)
                GiftCardCode.objects.filter(code__in=code_list).update(status='1')
                res['status'] = 0
        except Exception as e:
            print(e)
            LogWx.objects.create(
                type='6',
                errmsg=e,
                errcode='6',
                remark='wx_order_id:{order}'.format(order=order_id)
            )
            res['status'] = 1
    else:
        LogWx.objects.create(
            type='6',
            errmsg=rep_data['errmsg'],
            errcode=rep_data['errcode'],
            remark='wx_order_id:{order}'.format(order=order_id)
        )
        res['status'] = 1

    return res


def user_gifting_card(wx_card_id):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        method.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    url = 'https://api.weixin.qq.com/card/code/update?access_token={token}' \
        .format(token=access_token)
    data = {
        "code": "12345678",
        "card_id": wx_card_id,
        "new_code": "3495739475"
    }