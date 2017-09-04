# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/28 15:58'
import datetime

from django.shortcuts import render
from django.views.generic.base import View

from admin.utils.paginator import MyPaginator
from admin.models import ShopOrder,ShopOrderInfo


class OrderView(View):
    def get(self,request,page):
        page_num = 1
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            orders = ShopOrder.objects.extra(select={
                'customer':'SELECT name FROM shop_address WHERE shop_address.openid=shop_order.customer'
            }).values('sn', 'price', 'save_time', 'status','customer','snap_address','tel')\
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