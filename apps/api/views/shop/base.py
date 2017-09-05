# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/28 16:56'
import json

from django.http import HttpResponse
from django.core.cache import caches

from admin.models import ShopBannerInfo,ShopTheme,ShopThemeInfo,ShopGood,ShopGoodImg,ShopGoodProperty,\
    ShopCategory
from utils import method


def getBannerById(request,b_id):
    try:
        banner = ShopBannerInfo.objects.values('img','target_id','type').filter(banner=b_id)
        res = method.createResult(0,'ok',{'banners':list(banner)})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))

    return HttpResponse(json.dumps(res))


def getThemes(request):
    theme_ids = request.GET.get('ids','')
    theme_ids = theme_ids.split(',')
    try:
        themes = ShopTheme.objects.values('img','id','name').filter(id__in=theme_ids)
        res = method.createResult(0, 'ok', {'themes': list(themes)})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))

    return HttpResponse(json.dumps(res))


def getThemeById(request,t_id):
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


def getCategories(request):
    try:
        categories = ShopCategory.objects.values('id','name','banner').filter(status='0').order_by('sort')
        res = method.createResult(0, 'ok', {'categories': list(categories)})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))
    return HttpResponse(json.dumps(res))


def getCategoryById(request,c_id):
    try:
        category = ShopCategory.objects.values('banner').get(pk=c_id)
        goods = ShopGood.objects.values('id','sn','name','price','img').filter(category=c_id)
        for good in goods:
            good['price'] = float(good['price'])
        data = {}
        data['banner'] = category['banner']
        data['items'] = list(goods)
        res = method.createResult(0, 'ok', {'category': data})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))
    return HttpResponse(json.dumps(res))


def getNewGood(request):
    try:
        goods = ShopGood.objects.values('id','sn','name','price','img').filter(is_new=1)
        for good in goods:
            good['price'] = float(good['price'])
        res = method.createResult(0, 'ok', {'goods': list(goods)})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))

    return HttpResponse(json.dumps(res))


def getGoodBySn(request,g_sn):
    try:
        good = ShopGood.objects.values('id','sn','name','price','img','stock').get(sn=g_sn)
        good['price'] = float(good['price'])
        imgs = ShopGoodImg.objects.values().filter(good_sn=g_sn)
        propertys = ShopGoodProperty.objects.values().filter(good_sn=g_sn)
        data = {}
        data['good'] = good
        data['imgs'] = list(imgs)
        data['properties'] = list(propertys)
        res = method.createResult(0, 'ok', {'good': data})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))

    return HttpResponse(json.dumps(res))


def getShopList(request):
    shops = caches['default'].get('base_shopDict','')
    print(shops)
    if shops:
        shop_name_list = []
        for code,name in shops.items():
            if code[0:1] in ('C','T') and code not in ('C00L','CM01'):
                shop_name_list.append(name)
        res = method.createResult(0, 'ok', {'shop_list': shop_name_list})
    else:
        res = method.createResult(1, 'base_shopDict in cache is empty')
    return HttpResponse(json.dumps(res))
