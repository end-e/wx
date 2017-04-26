# -*- coding:utf-8 -*-
from datetime import datetime
import time

from django.core.exceptions import ObjectDoesNotExist
from wechatpy import WeChatClient

from .models import AccessToken
from apps.utils import consts


def get_access_token_job():
    # 当前时间，时间戳格式
    current_time = time.mktime(datetime.now().timetuple())

    # 微信appid, appsecret
    appid = consts.APPID
    appsecret = consts.APPSECRET

    try:
        # AccessToken 生成时间
        obj = AccessToken.objects.get(pk=1)
        add_time = obj.add_time
        # 将%Y-%m-%d %H:%M:%S 转换成时间戳
        add_time = time.mktime(time.strptime(str(add_time), "%Y-%m-%d %H:%M:%S"))

        if current_time - add_time >= 1800:
            component = WeChatClient(appid, appsecret)
            result = component.fetch_access_token()

            obj.access_token = result['access_token']
            obj.expires_in = result['expires_in']
            # 将时间戳转换成日期格式
            obj.add_time = datetime.fromtimestamp(current_time)
            obj.save()
    except ObjectDoesNotExist:
        component = WeChatClient(appid, appsecret)
        result = component.fetch_access_token()
        AccessToken.objects.create(access_token=result['access_token'], expires_in=result['expires_in'])
