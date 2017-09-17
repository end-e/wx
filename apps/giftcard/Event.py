# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/5 17:40'
import json,requests

from django.db import transaction

from admin.utils.myClass import MyException
from admin.models import GiftCardCode,GiftOrder,GiftOrderInfo
from api.models import LogWx
from django.core.cache import caches
from utils import consts,wx,giftcard
from admin.utils import method

@transaction.atomic
def giftcard_pay_done(order_id):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        wx.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    rep_data = giftcard.getOrder(access_token, order_id)

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
                #
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
                # 更改guest状态
                res_guest = method.updateCardMode(code_list, 9, 1)
                if res_guest['status'] == 1:
                    raise MyException('订单'+order_id+'中的code,在guest中状态更新失败')
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
        wx.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    url = 'https://api.weixin.qq.com/card/code/update?access_token={token}' \
        .format(token=access_token)
    data = {
        "code": "12345678",
        "card_id": wx_card_id,
        "new_code": "3495739475"
    }