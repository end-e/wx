# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 13:53'
import requests,json

from django.core.cache import caches
from django.http import HttpResponse
from wechatpy import WeChatClient

from utils import consts
from api.models import LogWx

appId = consts.WX_APP_ID
appSecret = consts.WX_APP_SECRET

def getWxUserInfo(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': appId,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    rep = requests.get(url,params=params)

    rep_data = json.loads(rep.text)

    return rep_data

def get_access_token(app_name, app_id, secret):
    client = WeChatClient(app_id, secret)
    response = client.fetch_access_token()
    token = response['access_token']
    key = 'wx_{app_name}_access_token'.format(app_name=app_name)
    caches['default'].set(key, token, 7200)

    return token


def send_temp(msg):
    # 用户openid
    user_id = msg['openid']
    app_id = msg['app_id']
    secret = msg['secret']
    access_token = msg['access_token']
    data = msg['data']

    client = WeChatClient(app_id, secret, access_token)
    message = client.message
    # 模版id
    template_id = 'eddBYOpWHXKIiZ0IW74uUrDGUyBwjgjwSq1C5s-j_uo'

    mini_program = {
        'appid': consts.WX_APP_ID,
        'pagepath': 'pages/index/index'
    }
    res_send = message.send_template(user_id, template_id, data, None, mini_program)

    if res_send['errmsg'] != 'ok':
        LogWx.objects.create(
            type='1',
            remark='openid:' + user_id,
            errmsg=res_send['errmsg'],
            errcode=res_send['errcode']
        )


def respondToWx(flag):
    httpResponse = HttpResponse()
    if flag:
        httpResponse.status_code = 200
        content = '<xml>ok</xml>'
    else:
        httpResponse.status_code = 500
        content = '<xml>fail</xml>'
    httpResponse.content = content
    return httpResponse