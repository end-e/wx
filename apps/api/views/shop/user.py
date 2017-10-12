# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/9/4 13:38'
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from admin.models import ShopUser,ShopAddress
from utils import method,shop
from utils.myClass import MyException
from user.models import WechatMembers
from api.decorator import signature2


@csrf_exempt
@signature2
def userSave(request):
    nickname = request.POST.get('nickname','')
    nickname = nickname.encode('utf-8')
    extend = request.POST.get('extend','')
    wxUser= shop.getWxUser(request)
    openid = wxUser['openid']
    unionid = wxUser['unionid']
    res = {}
    try:
        user = ShopUser.objects.filter(unionid=unionid)
        if user.exists():
            user.update(nickname=nickname,extend=extend)
        else:
            ShopUser.objects.create(openid=openid,unionid=unionid,nickname=nickname,extend=extend)
            res = method.createResult(0, 'ok')
    except Exception as e:
        print(e)
        res = method.createResult(1, e.args[0])

    return HttpResponse(json.dumps(res))


@signature2
def getuserInfo(request):
    openid = shop.getWxUserOpenID(request)
    try:
        user = ShopUser.objects.values('nickname','kg_money','openid').get(openid=openid)
        res = method.createResult(0, 'ok', {'user': user})
    except Exception as e:
        res = method.createResult(1, e.args[0])

    return HttpResponse(json.dumps(res))


@signature2
def getUserAddresses(request):
    openid = shop.getWxUserOpenID(request)
    try:
        addresses = ShopAddress.objects.values('name','tel','province','city','country','detail','is_default')\
            .filter(openid=openid)
        res = method.createResult(0, 'ok',{'addresses':list(addresses)})
    except Exception as e:
        print(e)
        res = method.createResult(1, e.args[0])
    return HttpResponse(json.dumps(res))


@csrf_exempt
@signature2
def userAddressEdit(request):
    openid = shop.getWxUserOpenID(request)
    name = request.POST.get('name','')
    province = request.POST.get('province','')
    city = request.POST.get('city','')
    country = request.POST.get('country','')
    mobile = request.POST.get('mobile','')
    detail = request.POST.get('detail','')
    try:
        qs_address = ShopAddress.objects.filter(openid=openid)
        if qs_address.exists():
            qs_address.update(name=name,tel=mobile,province=province,city=city,country=country,detail=detail)
        else:
            ShopAddress.objects.create(
                openid=openid,name=name,tel=mobile,province=province,city=city,country=country,detail=detail
            )
        res = method.createResult(0, 'ok')
    except Exception as e:
        print(e)
        res = method.createResult(1, e.args[0])

    return HttpResponse(json.dumps(res))


@signature2
def getUserKgMoney(request):
    openid = shop.getWxUserOpenID(request)
    try:
        user = ShopUser.objects.values('kg_money').get(openid=openid)
        kg_money = user['kg_money']
        res = method.createResult(0, 'ok', {'kg_money': kg_money,'openid':openid})
    except Exception as e:
        print(e)
        res = method.createResult(1, e.args[0])
    return HttpResponse(json.dumps(res))


@signature2
def getUserPoint(request):
    wxUser = shop.getWxUser(request)
    openid = wxUser['openid']
    unionid = wxUser['unionid']
    res = {}
    try:
        member = WechatMembers.objects.values('membernumber').filter(unionid=unionid).first()
        if member:
            member_id = member['membernumber']
            res['member_id'] = member_id
            guest = shop.getGuest(member_id)
            if not guest:
                raise MyException('the card is abnormal')
            point = float(guest['point'])
            res = method.createResult(0, 'ok', {'point': point, 'openid': openid})
        else:
            res = method.createResult(1, 'the member is not in WechatMembers')
    except Exception as e:
        print(e)
        res = method.createResult(2, e.args[0])
    finally:
        return HttpResponse(json.dumps(res))
