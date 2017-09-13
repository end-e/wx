# -*- coding: utf-8 -*-
import time
import os
import requests
import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import JsonResponse

from admin.utils.paginator import MyPaginator
from cash_coupons.models import CashCouponsImg
from apps.admin.utils.myClass import MyViewIkg
from .forms import UploadFileForm


# class CashCouponsListView(View):
#     def get(self, request):
#         return render(request, 'cash_coupons/cash_coupons_list.html', {})


class CashCouponsStoreListView(View):
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


class CashCouponsImgListView(View):
    """
    图片素材列表
    """

    def get(self, request):
        img_name = request.GET.get('name', '')

        if img_name:
            all_imgs = CashCouponsImg.objects.filter(title__icontains=img_name).order_by('-create_time')
        else:
            all_imgs = CashCouponsImg.objects.all().order_by('-create_time')

        paginator = MyPaginator(all_imgs, 10)
        page_num = request.GET.get('page', 1)
        try:
            all_imgs = paginator.page(page_num)
        except Exception as e:
            print(e)
        return render(request, 'cash_coupons/cash_coupons_img_list.html', {
            'all_imgs': all_imgs
        })


class CashCouponsImgUploadView(View):
    """
    素材图片详情
    """

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'cash_coupons/cash_coupons_img_upload.html', locals())

    def post(self, request):
        access_token = MyViewIkg().token
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}' \
            .format(access_token=access_token)

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            mypic = request.FILES.get('img', '')
            ext = os.path.splitext(mypic.name)[1]
            mypic.name = str(int(time.time())) + ext
            files = {'file': mypic}

            rep = requests.post(url, files=files)
            rep_data = json.loads(rep.text)

            res = {}
            if 'url' in rep_data.keys():
                cdn_url = rep_data['url']
                try:
                    img_id = request.POST.get('img_id', '')
                    if img_id:
                        CashCouponsImg.objects.filter(id=img_id).update(title=title, url=cdn_url)
                    else:
                        CashCouponsImg.objects.create(title=title, url=cdn_url)
                    return redirect(reverse('cash_coupons/cash_coupons_img_list.html'))
                except Exception as e:
                    print(e)
                    pass
            else:
                res['status'] = 1
                res['msg'] = rep_data['errmsg']
            return render(request, 'cash_coupons/cash_coupons_img_upload.html', locals())


class CashCouponsImgDetailView(View):
    def get(self, request, img_id):
        img = CashCouponsImg.objects.get(id=int(img_id))
        return render(request, 'cash_coupons/cash_coupons_img_upload.html', {
            'img': img
        })


class CashCouponsImgStatusView(View):
    def get(self, request, status, img_id):
        img_status = CashCouponsImg.objects.filter(id=int(img_id)).update(status=status)
        res = {}
        if img_status:
            res['status'] = 0
        else:
            res['status'] = 1
        return JsonResponse(res)
