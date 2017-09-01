# -*-  coding:utf-8 -*-
# __author__ = ''
from django.views.generic.base import View
from django.core.cache import caches

from utils import wx, consts


class MyView(View):
    def __init__(self, **kwargs):
        super(MyView, self).__init__(**kwargs)
        access_token = caches['default'].get('wx_kgcs_access_token', '')
        if not access_token:
            wx.get_access_token('kgcs', consts.KG_APPID, consts.KG_APPSECRET)
        self.token = access_token


class MyViewIkg(View):
    def __init__(self, **kwargs):
        super(MyViewIkg, self).__init__(**kwargs)
        access_token = caches['default'].get('wx_ikg_access_token', '')
        if not access_token:
            wx.get_access_token('ikg', consts.APPID, consts.APPSECRET)
        self.token = access_token


class MyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
