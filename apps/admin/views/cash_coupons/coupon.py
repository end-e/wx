# -*- coding: utf-8 -*-
import time
import os
import requests
import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from apps.admin.utils.myClass import MyViewIkg
from .forms import CashCouponsAddForm
from utils import data



class CouponsListView(View):
    def get(self, request):
        # coupons =
        return render(request, 'cash_coupons/cash_coupons_list.html', locals())


class CouponsAddView(View):
    def get(self, request):
        return render(request, 'cash_coupons/cash_coupons_add.html', locals())

    def post(self, request):
        form = CashCouponsAddForm(request.POST)
        res = {}

        if form.is_valid():
            try:
                res_save = form.save()
                return redirect(reverse('admin:cash_coupons:coupons'))
            except Exception as e:
                res['status'] = 1
        else:
            res['status'] = 1
        return render(request, 'cash_coupons/cash_coupons_add.html', locals())


class insertCouponView(View):
    def get(self,request):
        pass

    def post(self,request):
        coupon = (
            # shop, couponname, datetime.datetime.now(), endDate, float(costValue),
            # serial_id, coupon_code, name, range
        )
        data.insertCoupon(coupon)


class CouponsStoreListView(View):
    """
    获取微信后台的门店列表
    """

    def get(self, request):
        access_token = MyViewIkg().token
        url = 'https://api.weixin.qq.com/cgi-bin/poi/getpoilist?access_token={access_token}'.format(
            access_token=access_token)
        params = {'begin': 0, 'limit': 50}
        json_params = json.dumps(params, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, data=json_params)
        response_dict = response.json()

        if 'business_list' in response_dict:
            business_list = response_dict['business_list']

        return render(request, 'cash_coupons/store_list.html', locals())

