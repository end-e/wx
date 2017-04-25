# -*- coding:utf-8 -*-
import datetime

from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient

from apps.utils import consts
from .models import AccessToken


class WeChatAccessView(View):
    def get(self, request):
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        token = consts.TOKEN

        try:
            check_signature(token, signature, timestamp, nonce)
            return HttpResponse(echostr)
        except InvalidSignatureException:
            return HttpResponse(u'验证失败')


class GetAccessTokenView(View):
    def get(self, request):
        appid = consts.APPID
        appsecret = consts.APPSECRET
        component = WeChatClient(appid, appsecret)
        result = component.fetch_access_token()

        try:
            obj = AccessToken.objects.get(pk=1)
            obj.access_token = result['access_token']
            obj.expires_in = result['expires_in']
            obj.add_time = datetime.datetime.now()
            obj.save()
        except ObjectDoesNotExist:
            AccessToken.objects.create(access_token=result['access_token'], expires_in=result['expires_in'])

        return HttpResponse(result)
