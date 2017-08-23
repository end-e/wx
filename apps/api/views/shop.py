# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/28 16:56'
import json,datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F
from django.core.paginator import Paginator

from admin.models import ShopBannerInfo,ShopTheme,ShopThemeInfo,ShopGood,ShopGoodImg,ShopGoodProperty,\
    ShopOrder,ShopUser,ShopCategory,ShopAddress,ShopOrderInfo,ShopKgMoneyOrder
from utils import method
from utils.myClass import MyException
from user.models import WechatMembers


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


def userInfo(request,openid):
    user = ShopUser.objects.filter(openid=openid)
    res = {}
    if user.count()>0:
        res['status'] = 0
        res['data'] = user.values('nickname','kg_money','openid').first()
    else:
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
        res['data'] = list(orders)
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getUserKgMoney(request):
    openid = request.GET.get('openid','')
    res = {}
    try:
        user = ShopUser.objects.values('kg_money').get(openid=openid)
        kg_money = user['kg_money']
        res['status'] = 0
        res['kg_money'] = kg_money
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))


def getUserPoint(request):
    openid = request.GET.get('openid','')
    res = {}
    try:
        member = WechatMembers.objects.values('membernumber').get(openid=openid)
        member_id = member['membernumber']
        res['member_id'] = member_id
        point = method.getGuestPoint(member_id)
        res['status'] = 0
        res['point'] = point
    except Exception as e:
        print(e)
        res['status'] = 1
    return HttpResponse(json.dumps(res))

@csrf_exempt
def orderGoodsSave(request):
    openid = request.POST.get('openid','')
    goods = request.POST.get('goods','')
    goods = json.loads(goods)
    price = request.POST.get('totalPrice','')
    address = request.POST.get('address','')
    user_name = request.POST.get('user','')
    tel = request.POST.get('tel','')

    res = {}
    user= ShopUser.objects.values('kg_money').get(openid=openid)
    kg_money = user['kg_money']
    if kg_money<int(price):
        res['status'] = 2
        return HttpResponse(json.dumps(res))
    try:
        with transaction.atomic():
            # 0、获取订单编号
            sn = method.createOrderSn(ShopOrder)
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
                name=user_name, tel=tel, snap_address=address
            )
            # 创建商品信息
            ShopOrderInfo.objects.bulk_create(info_list)
            #2、更新用户余额
            ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money') - int(price))
            res['status'] = 0
            res['order_sn'] = sn
    except Exception as e:
        print(e)
        res['status'] = 1
        if hasattr(e,'value'):
            err = e.value.split(':')
            res['status'] = err[0]
            res['msg'] = err[1]


    return HttpResponse(json.dumps(res))


@csrf_exempt
def orderKgMoneySave(request):
    openid = request.POST.get('openid', '')
    kg_money = request.POST.get('kgMoney', 0)
    pay_type = request.POST.get('payType', '0')
    total_pay = request.POST.get('totalPay', 0)

    res = {}
    try:
        with transaction.atomic():
            if pay_type not in ('0','1'):
                raise MyException('支付类型错误')
            # 0、获取订单编号并新建订单
            sn = method.createOrderSn(ShopKgMoneyOrder)
            ShopKgMoneyOrder.objects.create(
                sn = sn, count = kg_money, pay_type = pay_type, price = total_pay, customer = openid
            )

            #guest中查询会员积分数量
            member = WechatMembers.objects.values('membernumber').filter(openid=openid).first()
            if member:
                if pay_type == '0':
                    member_id = member['membernumber']
                    point = method.getGuestPoint(member_id)
                    if float(point)< float(total_pay):
                        res['status'] = 1
                        res['msg'] = '积分余额不足'
                        return HttpResponse(json.dumps(res))
                    else:
                        # 消减会员积分
                        res_update = method.updateGuestPoint(member_id,total_pay)
                        if not res_update :
                            raise MyException('会员积分消减失败')
                        #增加会员宽广豆数量
                        ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money')+int(kg_money))
            else:
                raise MyException('微查询到此openid对应的会员')
            res['status'] = 0
            res['order_sn'] = sn
    except Exception as e:
        print(e)
        res["status"] = 1
        if hasattr(e, 'value'):
            res['msg'] = e.value
        else:
            res['msg'] = e

    return HttpResponse(json.dumps(res))


@csrf_exempt
def userOrderReSave(request):
    openid = request.POST.get('openid','')
    sn = request.POST.get('sn','')
    price = request.POST.get('totalPrice', '')
    res ={}
    try:
        with transaction.atomic():
            ShopOrder.objects.filter(sn=sn).update()
            res['status'] = 0
            res['order_sn'] = sn

            ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money')-int(price))
    except Exception as e:
        print(e)
        res['status'] = 1

    return HttpResponse(json.dumps(res))


def getOrderBySn(request):
    """
    获取用户订单
    :param sn:订单编号
    :param order_type:订单类型（0：商品订单；1：宽广豆订单 ）
    :return:
    """
    sn = request.GET.get('sn','')
    order_type = request.GET.get('type','')
    res = {}
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





































