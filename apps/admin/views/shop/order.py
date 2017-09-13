# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/28 15:58'
import datetime,json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from admin.utils.paginator import MyPaginator
from admin.models import ShopOrder,ShopOrderInfo, ShopKgMoneyOrder
from utils import method


class OrderView(View):
    def get(self,request,page):
        page_num = 1
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            orders = ShopOrder.objects.values('sn', 'price', 'save_time', 'status','snap_address','tel','express','name')\
                .order_by('-save_time')
            paginator = MyPaginator(orders, 6)
            page = int(page) if int(page) else 1
            orders = paginator.page(page)
            for order in orders:
                order['price'] = float(order['price'])
                order['save_time'] = datetime.datetime.strftime(order['save_time'], '%Y-%m-%d %H:%M:%S')
                info = ShopOrderInfo.objects.extra(select={
                    'good_name':'SELECT name FROM shop_good WHERE shop_good.sn=shop_order_info.good_sn'
                }).values('good_name','good_num').filter(order_sn=order['sn'])
                if info:
                    order['items'] = info
        except Exception as e:
            print(e)

        return render(request,'shop/order_list.html',locals())


class UpdateStatus(View):
    def post(self,request):
        sn = request.POST.get('sn','')
        status = request.POST.get('status','')
        if status == '7':
            express = request.POST.get('express','')
            if express=='1':
                express_sn = request.POST.get('express_sn','')
                if not express_sn:
                    res =  method.createResult(1,'express_sn is require')
                    return HttpResponse(json.dumps(res))
                else:
                    res_rows = ShopOrder.objects.filter(sn=sn).update(status=status,express_sn=express_sn)
            else:
                res_rows = ShopOrder.objects.filter(sn=sn).update(status=status)
        else:
            res_rows = ShopOrder.objects.filter(sn=sn).update(status=status)
        if res_rows!=1:
            res = method.createResult(1,'order update status failed')
        else:
            res = method.createResult(0,'ok')

        return HttpResponse(json.dumps(res))


class KgMoneyOrderView(View):
    def get(self,request,page):
        page_num = 1
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            orders = ShopKgMoneyOrder.objects.extra(select={
                'name':'SELECT name FROM shop_address WHERE shop_address.openid=shop_kgmoney_order.customer'
            }).values('sn', 'count', 'pay_type', 'price','name','status','save_time')\
                .order_by('-save_time')
            paginator = MyPaginator(orders, 6)
            page = int(page) if int(page) else 1
            orders = paginator.page(page)
            for order in orders:
                order['price'] = float(order['price'])
                order['save_time'] = datetime.datetime.strftime(order['save_time'], '%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(e)

        return render(request,'shop/kgmoney_order_list.html',locals())