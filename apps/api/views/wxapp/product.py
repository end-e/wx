# -*- coding: utf-8 -*-
import json, datetime
from django.http import HttpResponse
from wxapp.models import Product
from wxapp.constants import MEDIA_URL
from api.decorator import signature


@signature
def getProductList(request):
    result_dict = {'status': 1, 'msg': []}

    kwargs = {}

    kwargs.setdefault('enable_flag', '0')
    kwargs.setdefault('begin_date__lte', datetime.datetime.now())
    kwargs.setdefault('end_date__gte', datetime.datetime.now())

    products = Product.objects.filter(**kwargs)
    msg = []

    if products:
        for item in products:
            vardict = {}
            vardict['product_id'] = str(item.id)
            vardict['product_code'] = str(item.product_code)
            vardict['product_name'] = str(item.product_name)
            vardict['price'] = str(item.price)
            vardict['stock'] = str(item.stock)
            vardict['type_flag'] = str(item.type_flag)
            vardict['product_weight'] = str(item.product_weight)
            vardict['begin_date'] = str(item.begin_date.strftime("%Y-%m-%d"))
            vardict['end_date'] = str(item.end_date.strftime("%Y-%m-%d"))
            vardict['product_image'] = MEDIA_URL + str(item.product_image)
            msg.append(vardict)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")


@signature
def getProductInfo(request):
    result_dict = {'status': 1, 'msg': []}

    product_id = request.GET.get('product_id', '')

    product = Product.objects.get(pk=product_id, enable_flag='0')
    msg = {}

    if product:
        msg['id'] = str(product.id)
        msg['product_code'] = str(product.product_code)
        msg['product_name'] = str(product.product_name)
        msg['price'] = str(product.price)
        msg['stock'] = str(product.stock)
        msg['type_flag'] = str(product.type_flag)
        msg['product_weight'] = str(product.product_weight)
        msg['begin_date'] = str(product.begin_date.strftime("%Y-%m-%d"))
        msg['end_date'] = str(product.end_date.strftime("%Y-%m-%d"))
        msg['product_image'] = MEDIA_URL + str(product.product_image)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")
