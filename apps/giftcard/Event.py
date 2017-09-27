# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/5 17:40'
from django.db import transaction

from django.core.cache import caches
from utils import consts,wx,giftcard
from admin.utils import method
from utils import data

@transaction.atomic
def giftcard_pay_done(order_id):
    access_token = caches['default'].get('wx_kgcs_access_token', '')
    if not access_token:
        wx.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)

    rep_data = giftcard.getOrder(access_token, order_id)
    res = {'status':0}
    if rep_data['errcode'] == 0:
        order = rep_data['order']
        data.saveAndUpdateLocalData(order)
    else:
        method.CreateLog('6',rep_data['errcode'],rep_data['errmsg'],order_id)
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