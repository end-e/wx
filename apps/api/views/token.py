# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 13:50'
import hashlib,json,time

from django.http import HttpResponse
from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt

from utils import wx,method


@csrf_exempt
def getToken(request):
    code = request.POST.get('code','')
    openid = wx.getOpenIdByCode(code)
    key = method.createNonceStr(32)
    tamp = int(time.time())
    key = key+code+str(tamp)
    key = hashlib.md5(key.encode(encoding='utf-8')).hexdigest()
    flag = caches['default'].set(key,openid,7200)

    if flag:
        res = method.createResult(0,'ok',{'token':key})
    else:
        res = method.createResult(1, 'openid cache failed')

    return HttpResponse(json.dumps(res))


@csrf_exempt
def verify(request):
    token = request.POST.get('token','')
    if token:
        wxUser = caches['default'].get(token, '')
        if wxUser:
            res = method.createResult(0, 'ok')
        else:
            res = method.createResult(1, 'token is not exist or is expired')
    else:
        res = method.createResult(1, 'token in request is null')
    return HttpResponse(json.dumps(res))




