import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import caches
from django.views.generic.base import View

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient
from utils import consts


def conn(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echostr = request.GET.get('echostr', '')
    token = 'ikuanguang'
    try:
        check_signature(token, signature, timestamp, nonce)
        return HttpResponse(echostr)
    except InvalidSignatureException:
        return HttpResponse(u'验证失败')


def hx(request, sn, stamp):
    """
    微信卡卷核销
    :param request:
    :param sn: 卡卷编码
    :param stamp: 发送核销请求时间
    :return:
    """
    if sn:
        # TODO 查询核销状态
        state = caches['default'].get(sn, '')
        if not state:
            # TODO 向微信请求核销卡卷
            token = get_token()
        else:
            pass

    else:
        # TODO
        pass


def get_token():
    token = caches['default'].get('token', '')
    # 如果不存在，请向微信请求获取
    if not token:
        app_id = 'wxd892ee844883f6a8'
        secret = '8888eb81688a37912e05ba0520ac4b70'
        client = WeChatClient(app_id, secret)
        response = client.fetch_access_token()
        token = response['access_token']
        time = datetime.datetime.now()
        caches['default'].set('token', token)

    return token


def check_consume(code, token):
    pass


def get_template_id(request):
    app_id = consts.APPID
    secret = consts.APPSECRET
    client = WeChatClient(app_id, secret)

    message = client.message
    user_id = 'oE9Pts9_cBLTWccP682FgWuvQ7js'
    template_id = '0twv952J80MHBUm_WUQfgNPG9w7_FyALpYxSpAvgVjc'
    url = ''
    top_color = '#efefef'
    miniprogram = {}
    data = {
        "message": {
            "value": "恭喜你购买成功！",
            "color": "#173177"
        },
        "message2": {
            "value": "巧克力",
            "color": "#173177"
        }
    }

    res_send = message.send_template(user_id, template_id, url, top_color, data)
    return HttpResponse(json.dumps(res_send))
