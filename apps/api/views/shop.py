# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/28 16:56'
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from admin.models import ShopBannerInfo,ShopTheme,ShopThemeInfo,ShopGood,ShopGoodImg,ShopGoodProperty,\
    ShopOrder,ShopUser,ShopCategory,ShopAddress,ShopOrder,ShopOrderInfo
from utils import method


def getBanner(request,b_id):
    res = {}
    try:
        banner = ShopBannerInfo.objects.values('img','target_id','type').filter(banner=b_id)
        res['status'] = 0
        res['items'] = list(banner)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getThemes(request):
    theme_ids = request.GET.get('ids','')
    theme_ids = theme_ids.split(',')
    res = {}
    try:
        themes = ShopTheme.objects.values('img','id','name').filter(id__in=theme_ids)
        res['status'] = 0
        res['items'] = list(themes)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getTheme(request,t_id):
    res = {}
    try:
        theme = ShopTheme.objects.values('banner').get(pk=t_id)
        theme_goods = ShopThemeInfo.objects.values('good_sn').filter(theme_id=t_id)
        good_sns = [theme_good['good_sn'] for theme_good in theme_goods]
        goods = []
        for good_sn in good_sns :
            good = ShopGood.objects.values('id','sn','name','price','img').get(sn=good_sn)
            good['price'] = float(good['price'])
            goods.append(good)

        res['status'] = 0
        data = {}
        data['img'] = theme['banner']
        data['goods'] = goods
        res['data'] = data

    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getGoodNew(request):
    res = {}
    try:
        goods = ShopGood.objects.values('id','sn','name','price','img').filter(is_new=1)
        res['status'] = 0
        for good in goods:
            good['price'] = float(good['price'])
        res['items'] = list(goods)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getGood(request,g_sn):
    res = {}
    try:
        good = ShopGood.objects.values('id','sn','name','price','img','stock').get(sn=g_sn)
        good['price'] = float(good['price'])
        imgs = ShopGoodImg.objects.values().filter(good_sn=g_sn)
        propertys = ShopGoodProperty.objects.values().filter(good_sn=g_sn)
        data = {}
        data['good'] = good
        data['imgs'] = list(imgs)
        data['properties'] = list(propertys)
        res['data']=data
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getOrderByUser(request):
    u_id = request.GET.get('u_id','')
    res = {}
    try:
        orders = ShopOrder.objects.values().filter(user=u_id)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


@csrf_exempt
def userSave(request):
    nickname = request.POST.get('nickname','')
    extend = request.POST.get('extend','')
    openid = request.POST.get('openid','')
    res = {}
    try:
        user = ShopUser.objects.filter(openid=openid)
        if user.count()>0:
            user.update(nickname=nickname,extend=extend)
        else:
            ShopUser.objects.create(openid=openid,nickname=nickname,extend=extend)
        res['status'] = 0
    except Exception as e:
        res['status'] = 0
        print(e)

    return HttpResponse(json.dumps(res))


def getUserAddresses(request,openid):
    res = {}
    try:
        addresses = ShopAddress.objects.values('name','tel','province','city','country','detail','is_default')\
            .filter(openid=openid)
        res['data'] = list(addresses)
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))


@csrf_exempt
def userAddressEdit(request,openid):
    name = request.POST.get('name','')
    province = request.POST.get('province','')
    city = request.POST.get('city','')
    country = request.POST.get('country','')
    mobile = request.POST.get('mobile','')
    detail = request.POST.get('detail','')
    res = {}
    try:
        qs_address = ShopAddress.objects.filter(openid=openid)
        if qs_address.count()>0:
            qs_address.update(name=name,tel=mobile,province=province,city=city,country=country,detail=detail)
        else:
            ShopAddress.objects.create(
                openid=openid,name=name,tel=mobile,province=province,city=city,country=country,detail=detail
            )
        res['status'] = 0
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getUserOrders(request,openid,page):
    res = {}
    try:
        orders = ShopOrder.objects.values('sn','price','status').filter(customer=openid)
        for order in orders:
            count = ShopOrderInfo.objects.filter(order_sn=order['sn']).count()
            order['count'] = count
        res['data'] = list(orders)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


@csrf_exempt
def userOrderEdit(request):
    openid = request.POST.get('openid','')
    goods = request.POST.get('goods','')
    goods = json.loads(goods)
    price = request.POST.get('totalPrice','')
    res ={}
    try:
        with transaction.atomic():
            sn = method.createOrderSn()
            ShopOrder.objects.create(
                customer = openid,sn=sn,price=price
            )
            info_list = []
            for good in goods:
                info = ShopOrderInfo()
                info.order_sn = sn
                info.good_sn = good['sn']
                info.good_num = good['counts']
                info_list.append(info)
            ShopOrderInfo.objects.bulk_create(info_list)
            res['status'] = 0
            res['order_sn'] = sn
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getUserOrder(request,openid,sn):
    res = {}
    try:
        orders = ShopOrder.objects.values('sn','price','save_time').filter(customer=openid)
        res['data'] = list(orders)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getOrder(request,sn):
    res = {}
    try:
        order = ShopOrder.objects.values('sn','price').get(sn=sn)
        info_list = ShopOrderInfo.objects.values('good_sn','good_num')
        goods = []
        for info in info_list:
            good =ShopGood.objects.values('img','price','name').get(sn=info['good_sn'])
            good['price'] = float(good['price'])
            good['count'] = info['good_num']
            goods.append(good)

        data = {'sn':order['sn'],'account':float(order['price']),'goods':goods}
        res['status'] = 0
        res['data'] = data
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))


def getCategories(request):
    res = {}
    try:
        categories = ShopCategory.objects.values('id','name','banner').filter(status='0').order_by('sort')
        res['data'] = list(categories)
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))


def getCategoryInfo(request,c_id):
    res = {}
    try:
        category = ShopCategory.objects.values('banner').get(pk=c_id)
        goods = ShopGood.objects.values('id','sn','name','price','img').filter(category=c_id)
        for good in goods:
            good['price'] = float(good['price'])
        data = {}
        data['banner'] = category['banner']
        data['items'] = list(goods)
        res['data'] = data
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))





































