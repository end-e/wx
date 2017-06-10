import json
import datetime
import requests
from urllib import parse

from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import caches

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient, WeChatOAuth
from utils import consts


def conn(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echostr = request.GET.get('echostr', '')
    token = 'giftcard'
    try:
        check_signature(token, signature, timestamp, nonce)
        return HttpResponse(echostr)
    except InvalidSignatureException:
        return HttpResponse(u'验证失败')


def get_token():
    token = caches['default'].get('giftcard_access_token', '')
    # 如果不存在，请向微信请求获取
    if not token:
        app_id = 'wx818828d30e21a3c4'
        secret = 'e647abf81b3337de38539d7f7807e39e'
        client = WeChatClient(app_id, secret)
        response = client.fetch_access_token()
        token = response['access_token']
        time = datetime.datetime.now()
        caches['default'].set('giftcard_access_token', token)

    return token
