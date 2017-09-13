# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/23 9:46'
import time

from django import template

from admin.models import ShopGood,ShopBanner

register = template.Library()


@register.filter('range')
def to_list(value):
    return range(1, int(value)+1)


@register.filter('int')
def to_int(val):
    return int(val)


#加法：v1 + v2
@register.filter
def add(v1,v2):
    return float(v1) + float(v2)


#减法：v1 - v2
@register.filter
def subtract(v1,v2):
    return float(v1) - float(v2)


#乘法：v1 * v2
@register.filter
def multiply(v1,v2):
    return float(v1) * float(v2)


#除法：v1 / v2
@register.filter
def divide(v1,v2):
    return float(v1) / float(v2)


 #取余：v1 % v2
@register.filter
def remainder(v1,v2):
    return float(v1) % float(v2)


@register.filter
def toDate(data):
    x = time.localtime(float(data))
    return time.strftime('%y-%m-%d %H:%M:%S', x)


@register.filter
def getListItem(str,index):
    list = str.split(':')
    return list[index]


@register.filter
def toGoodName(sn):
    good = ShopGood.objects.values('name').get(sn=sn)
    return good['name']


@register.filter
def toBannerName(id):
    banner = ShopBanner.objects.get(pk=id)
    return banner.name


@register.filter
def toBannerInfoTypeName(type):
    dict = {'0': '无跳转链接', '1': '商品链接', '2': '主题链接'}
    return dict[type]


@register.filter()
def toShopOrderStatus(status):
    dict = {'0':'未支付','7':'已发货','8':'已签收','9':'已支付'}
    return dict[status]


@register.filter()
def toShopOrderExpress(express):
    dict = {0:'门店自取',1:'快递配送'}
    return dict[express]