import json
import requests

from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient, parse_message

from utils import consts
from message import views as message_v


@csrf_exempt
def conn(request):
    if request.method == 'GET':
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
    elif request.method == 'POST':
        xml = request.body
        msg = parse_message(xml)
        return HttpResponse(message_v.switch_type(msg))


# 微信回调域名校验文件
def verify(request):
    return render(request, 'MP_verify_QthEcNlYA73MNXgH.txt')


# CA证书校验文件
def ca(request):
    return render(request, 'fileauth.txt')


def get_token():
    token = caches['default'].get('wx_ikg_access_token', '')
    # 如果不存在，请向微信请求获取
    if not token:
        app_id = 'wxd892ee844883f6a8'
        secret = '8888eb81688a37912e05ba0520ac4b70'
        client = WeChatClient(app_id, secret)
        response = client.fetch_access_token()
        token = response['access_token']
        caches['default'].set('wx_ikg_access_token', token, 7200)

    return token


def check_consume(code, token):
    pass


def create_nav(request):
    access_token = caches['default'].get('wx_ikg_access_token', '')
    if not access_token:
        access_token = get_token()

    # 配置自定义菜单
    client = WeChatClient(consts.APPID, consts.APPSECRET, access_token)

    # 配置自定义菜单
    menu_create = client.menu.create({
        "button": [
            {
                "type": "view",
                "name": "电子礼品卡",
                "url": "https://mp.weixin.qq.com/bizmall/giftcard?action=homepage&page_id=sO898gip2rDKIDXgaMcqTXSy64LOxmDMrEGdoxmrGeA%3d#wechat_redirect"
            },
            {
                "type": "view",
                "name": "宽广购",
                "url": "http://www.huigo.com/mobile"
            },
            {
                "name": "会员",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "会员卡",
                        "url": u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/membersimage&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
                    },
                    {
                        "type": "click",
                        "name": "消费记录",
                        "key": "xfjl"
                    },
                    {
                        "type": "view",
                        "name": "会员绑定",
                        "url": u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/membersbound&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
                    },
                    {
                        "type": "click",
                        "name": "解除绑定",
                        "key": "jcbd"
                    }
                ]
            }
        ]
    })
    return HttpResponse(json.dumps(menu_create))


def get_session_key(request):
    """
    小程序获取用户openid，使用小程序获取的code换取openid，session_key
    接口地址:
    https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    """
    appid = 'wxd5fbbceb077f7635'
    secret = '041e0f60a39e8b0ff699101142a6f849'

    code = request.GET.get('code', '')

    url = 'https://api.weixin.qq.com/sns/jscode2session'
    param = {
        'appid': appid,
        'secret': secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }

    res = requests.get(url, params=param)

    return HttpResponse(res, code)
