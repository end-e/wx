# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/9/4 13:38'
import json,datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F
from django.core.paginator import Paginator


from admin.models import ShopGood,ShopOrder,ShopUser,ShopOrderInfo,ShopKgMoneyOrder
from utils import method,shop
from utils.myClass import MyException
from user.models import WechatMembers
from api.decorator import signature2


@csrf_exempt
def orderGoodsSave(request):
    openid = shop.getWxUserOpenID(request)
    goods = request.POST.get('goods','')
    goods = json.loads(goods)
    price = request.POST.get('totalPrice','')
    address = request.POST.get('address','')
    user_name = request.POST.get('user','')
    tel = request.POST.get('tel','')
    express = request.POST.get('express','')

    res = {}
    user= ShopUser.objects.values('kg_money').get(openid=openid)
    kg_money = user['kg_money']
    if kg_money<int(price):
        res = method.createResult(3, '宽豆余额不足')
        return HttpResponse(json.dumps(res))
    try:
        with transaction.atomic():
            # 0、获取订单编号
            sn = shop.createOrderSn(ShopOrder)
            # 1、保存订单信息 更新商品库存
            info_list = []
            snap_name = []
            snap_img = []
            for good in goods:
                qs_good_list = ShopGood.objects.select_for_update().filter(sn=good['sn'])
                qs_good = qs_good_list.values('stock','name','img').first()
                stock = qs_good['stock']
                good_name = qs_good['name']
                #判断库存
                if stock>int(good['counts']):
                    #拼装订单快照信息
                    snap_name.append(good_name)
                    snap_img.append(qs_good['img'])
                    #组合订单商品信息
                    info = ShopOrderInfo()
                    info.order_sn = sn
                    info.good_sn = good['sn']
                    info.good_num = good['counts']
                    info_list.append(info)
                    #消减库存
                    qs_good_list.update(stock=F('stock') - int(good['counts']))
                else:
                    raise MyException('2:'+good_name)

            snap_name = '|'.join(snap_name)[0:63]
            snap_img = snap_img[0]

            #创建主表信息
            ShopOrder.objects.create(
                customer=openid, sn=sn, price=price, status='9',snap_img=snap_img,snap_name=snap_name,
                name=user_name, tel=tel, snap_address=address,express=express
            )
            # 创建商品信息
            ShopOrderInfo.objects.bulk_create(info_list)
            #2、更新用户余额
            ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money') - int(price))

            res = method.createResult(0,'ok', {'order_sn':sn})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))
        if hasattr(e,'value'):
            err = e.value.split(':')
            res = method.createResult(err[0],err[1])


    return HttpResponse(json.dumps(res))


@csrf_exempt
def orderKgMoneySave(request):
    openid = shop.getWxUserOpenID(request)
    kg_money = request.POST.get('kgMoney', 0)
    pay_type = request.POST.get('payType', '0')
    total_pay = request.POST.get('totalPay', 0)

    res = {}
    try:
        with transaction.atomic():
            if pay_type not in ('0','1'):
                raise MyException('支付类型错误')
            # 0、获取订单编号并新建订单
            sn = shop.createOrderSn(ShopKgMoneyOrder)
            ShopKgMoneyOrder.objects.create(
                sn = sn, count = kg_money, pay_type = pay_type, price = total_pay, customer = openid
            )

            #guest中查询会员积分数量
            member = WechatMembers.objects.values('membernumber').filter(openid=openid).first()
            point_now = 0
            if member:
                if pay_type == '0':
                    member_id = member['membernumber']
                    res_update = shop.updateGuestPoint(member_id,total_pay)
                    if res_update[0] == 0 :
                        point_now = res_update[3]
                    else:
                        raise MyException(res_update[1])

                    #增加会员宽广豆数量
                    ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money')+int(kg_money))
            else:
                raise MyException('微查询到此openid对应的会员')
            res = method.createResult(0, 'ok',{'order_sn':sn,'point':point_now})
    except Exception as e:
        print(e)
        if hasattr(e, 'value'):
            errmsg = e.value
        else:
            errmsg = e
        res = method.createResult(1, errmsg)

    return HttpResponse(json.dumps(res))


def getOrdersByUser(request,page):
    openid = shop.getWxUserOpenID(request)
    try:
        good_orders = ShopOrder.objects.extra(
            select={
                'count':'SELECT COUNT(*) FROM shop_order_info WHERE shop_order_info.order_sn=shop_order.sn',
                'type':'0'
            }
        ).values('sn', 'price', 'save_time', 'status','count','type').filter(customer=openid)

        money_orders = ShopKgMoneyOrder.objects.extra(select={'type':'1'}) \
            .values('sn', 'price', 'save_time', 'status','count','type').filter(customer=openid)
        orders = list(good_orders) + list(money_orders)
        orders = sorted(orders, key=lambda order: order['save_time'], reverse=True)
        paginator = Paginator(orders, 6)
        orders = paginator.page(page)
        for order in orders:
            order['price'] = float(order['price'])
            order['save_time'] = datetime.datetime.strftime(order['save_time'],'%Y-%m-%d %H:%M:%S')

        res = method.createResult(0, 'ok', {'orders': list(orders),'openid':openid})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))

    return HttpResponse(json.dumps(res))


def getOrderBySn(request):
    """
    获取用户订单
    :param sn:订单编号
    :param order_type:订单类型（0：商品订单；1：宽广豆订单 ）
    :return:
    """
    openid = shop.getWxUserOpenID(request)
    sn = request.GET.get('sn','')
    order_type = request.GET.get('type','')
    try:
        if order_type == '0':
            order = ShopOrder.objects.values('sn','price','status','save_time','snap_address','name','tel','snap_address')\
                .get(sn=sn)
            info_list = ShopOrderInfo.objects.values('good_sn','good_num').filter(order_sn=sn)
            goods = []
            for info in info_list:
                good =ShopGood.objects.values('img','price','name').get(sn=info['good_sn'])
                good['price'] = float(good['price'])
                good['count'] = info['good_num']
                goods.append(good)
        else:
            order = ShopKgMoneyOrder.objects.values('sn','price','count','status','save_time').get(sn=sn)
            goods = []
            good ={'img':'','price':float(order['price']),'name':'宽广豆','count':order['count']}
            goods.append(good)

        data = {'sn':order['sn'],'account':float(order['price']),'status':order['status'],
                'goods':goods,'save_time':datetime.datetime.strftime(order['save_time'],'%Y-%m-%d %H:%M:%S')}

        if order_type == '0':
            address = {'tel':order['tel'],'name':order['name'],'totalDetail':order['snap_address']}
            data['address'] = address

        res = method.createResult(0, 'ok', {'order': data,'openid':openid})
    except Exception as e:
        print(e)
        res = method.createResult(1, str(e))
    return HttpResponse(json.dumps(res))