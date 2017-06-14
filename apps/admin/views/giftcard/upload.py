# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/14 10:24'
from django.shortcuts import render
from django.views.generic.base import View
from django.core.cache import caches

from utils import method,consts

class UploadImgView(View):
    def post(self,request):
        access_token = caches['default'].get('wx_kgcs_access_token','')
        if not access_token:
            method.get_access_token('kgcs',consts.KG_APPID,consts.KG_APPSECRET)

        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}'\
            .format(access_token=access_token)

        data = request.urlopen(url, xml, timeout=second).read()
        return data


