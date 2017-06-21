# -*- coding: utf-8 -*-
import json, datetime

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from wxapp.models import Voucher, VoucherClass, Shops, DisCode
from wxapp.constants import MEDIA_URL
from api.decorator import signature


@signature
def getVoucherList(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')
    unit_price = request.GET.get('unit_price', '')
    voucher_price = request.GET.get('voucher_price', '')

    result_dict = {'status': 1, 'msg': []}

    kwargs = {}

    kwargs.setdefault('begin_date__lte', datetime.datetime.now())
    kwargs.setdefault('end_date__gte', datetime.datetime.now())

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    if unit_price != '':
        kwargs.setdefault('unit_price', unit_price)

    if voucher_price != '':
        kwargs.setdefault('voucher_price', voucher_price)

    vouchers = Voucher.objects.filter(**kwargs).order_by('voucher_no')
    msg = []
    if vouchers:
        for item in vouchers:
            vardict = {}
            vardict['voucher_id'] = str(item.id)
            vardict['voucher_no'] = str(item.voucher_no)
            vardict['voucher_name'] = str(item.voucher_name)
            vardict['unit_price'] = str(item.unit_price)
            vardict['voucher_price'] = str(item.voucher_price)
            vardict['goods_code'] = str(item.goods_code)
            vardict['type_flag'] = str(item.type_flag)
            vardict['code_flag'] = str(item.code_flag)

            code_list = []
            if vardict['code_flag'] == '0':
                var_shop = {}
                var_shop['shop_code'] = '0'
                var_shop['shop_name'] = '全部门店'
                code_list.append(var_shop)
            if vardict['code_flag'] == '1':
                var_shop = {}
                var_shop['shop_code'] = '1'
                var_shop['shop_name'] = '市区门店'
                code_list.append(var_shop)
            if vardict['code_flag'] == '2':
                var_shop = {}
                var_shop['shop_code'] = '2'
                var_shop['shop_name'] = '县区门店'
                code_list.append(var_shop)
            if vardict['code_flag'] == '3':
                if json.loads(item.shop_codes):
                    for itm in json.loads(item.shop_codes):
                        var_shop = Shops.objects.values('shop_code', 'shop_name').get(shop_code=itm['shop_code'])
                        code_list.append(var_shop)

            vardict['shop_codes'] = code_list

            vardict['begin_date'] = str(item.begin_date.strftime("%Y-%m-%d"))
            vardict['end_date'] = str(item.end_date.strftime("%Y-%m-%d"))
            vardict['voucher_image'] = MEDIA_URL + str(item.voucher_image)
            msg.append(vardict)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    # ensure_ascii=False 中文不序列化，utf-8编码
    return HttpResponse(json.dumps(result_dict, ensure_ascii=False).encode('utf-8'), content_type="application/json")


@signature
def getVoucherInfo(request):
    voucher_id = request.GET.get('voucher_id', '')

    result_dict = {'status': 1, 'msg': []}
    voucher = Voucher.objects.get(pk=voucher_id)

    msg = {}
    if voucher:
        msg['id'] = str(voucher.id)
        msg['voucher_no'] = str(voucher.voucher_no)
        msg['voucher_name'] = str(voucher.voucher_name)
        msg['unit_price'] = str(voucher.unit_price)
        msg['voucher_price'] = str(voucher.voucher_price)
        msg['goods_code'] = str(voucher.goods_code)
        msg['type_flag'] = str(voucher.type_flag)
        msg['code_flag'] = str(voucher.code_flag)

        code_list = []
        if msg['code_flag'] == '0':
            var_shop = {}
            var_shop['shop_code'] = '0'
            var_shop['shop_name'] = '全部门店'
            code_list.append(var_shop)
        if msg['code_flag'] == '1':
            var_shop = {}
            var_shop['shop_code'] = '1'
            var_shop['shop_name'] = '市区门店'
            code_list.append(var_shop)
        if msg['code_flag'] == '2':
            var_shop = {}
            var_shop['shop_code'] = '2'
            var_shop['shop_name'] = '县区门店'
            code_list.append(var_shop)
        if msg['code_flag'] == '3':
            if json.loads(voucher.shop_codes):
                for itm in json.loads(voucher.shop_codes):
                    var_shop = Shops.objects.values('shop_code', 'shop_name').get(shop_code=itm['shop_code'])
                    code_list.append(var_shop)

        msg['shop_codes'] = code_list

        msg['begin_date'] = str(voucher.begin_date.strftime("%Y-%m-%d"))
        msg['end_date'] = str(voucher.end_date.strftime("%Y-%m-%d"))
        msg['voucher_image'] = MEDIA_URL + str(voucher.voucher_image)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict, ensure_ascii=False).encode('utf-8'), content_type="application/json")


@signature
def getVoucherClass(request):
    result_dict = {'status': 1, 'msg': []}
    voucherClass = VoucherClass.objects.all()
    msg = []

    if voucherClass:
        for item in voucherClass:
            vardict = {}
            vardict['class_id'] = str(item.id)
            vardict['class_name'] = str(item.class_name)
            msg.append(vardict)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")


@signature
def verification_discode(request):
    discode = request.GET.get('discode', '')
    # 对discode进行切片，获取batch，dis_code
    batch = discode[:2]

    one_code = DisCode.objects.filter(batch=batch, dis_code=discode)

    if len(one_code) != 1:
        result_dict = {'status': 0, 'msg': 'failed'}
        return HttpResponse(json.dumps(result_dict), content_type="application/json")
    else:
        DisCode.objects.filter(batch=batch, dis_code=discode).update(has_usable=1, use_time=datetime.datetime.now())
        result_dict = {'status': 1, 'msg': 'success'}
        return HttpResponse(json.dumps(result_dict), content_type="application/json")
