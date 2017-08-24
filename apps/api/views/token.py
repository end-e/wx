# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 13:50'
import hashlib,json,time

from django.http import HttpResponse
from django.core.cache import caches

from utils import wx,method

def getToken(request):
    code = request.GET.get('code','')
    # openid = wx.getOpenIdByCode(code)
    openid = ''
    key = method.createNonceStr(32)
    tamp = int(time.time())
    key = key+'IiKkGg'+str(tamp)
    key = hashlib.md5(key.encode(encoding='utf-8')).hexdigest()
    flag = caches['default'].set(key,openid,7200)

    if flag:
        res = method.createResult(0,'ok',{'token':key})
    else:
        res = method.createResult(1, 'openid cache failed')

    return HttpResponse(json.dumps(res))

