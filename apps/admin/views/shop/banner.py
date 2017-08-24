# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/24 15:29'
import json,math

from django.shortcuts import render
from django.views.generic.base import View


from admin.models import ShopBanner,ShopBannerInfo
from admin.forms import ShopBannerForm,ShopBannerInfoForm
from admin.utils.paginator import MyPaginator

class BannerView(View):
    def get(self,request):
        banner_list = ShopBanner.objects.values().all().order_by('status','save_time')
        page_count = 10
        total_page = math.ceil(banner_list.count()/page_count)
        page = request.GET.get('page',1)
        paginator = MyPaginator(banner_list, page_count)
        banner_list = paginator.page(page)

        return render(request,'shop/banner_list.html',locals())


class BannerEditView(View):
    def get(self,request,b_id):
        if b_id != '0':
            banner = ShopBanner.objects.get(pk=b_id)
        return render(request, 'shop/banner_edit.html', locals())
    def post(self,request,b_id):
        if b_id == '0':
            form = ShopBannerForm(request.POST)
        else:
            qs_banner = ShopBanner.objects.get(pk=b_id)
            form = ShopBannerForm(request.POST,instance=qs_banner)

        res = {}
        if form.is_valid():
            res['status'] = 0
            try:
                form.save()
            except Exception as e:
                print(e)
                res['status'] = 1

        return render(request, 'shop/banner_edit.html', locals())


class BannerInfoView(View):
    def get(self,request,b_id):
        banner_info_list = ShopBannerInfo.objects.values().filter(banner=b_id).order_by('banner','sort')
        page_count = 10
        total_page = math.ceil(banner_info_list.count()/page_count)
        page = request.GET.get('page',1)
        paginator = MyPaginator(banner_info_list, page_count)
        banner_info_list = paginator.page(page)

        return render(request,'shop/banner_info_list.html',locals())


class BannerInfoEditView(View):
    def get(self,request,b_id,i_id):
        banner_list = ShopBanner.objects.values('id','name').filter(status='0')
        if i_id != '0':
            banner_info = ShopBannerInfo.objects.get(pk=i_id)
        return render(request,'shop/banner_info_edit.html',locals())

    def post(self,request,b_id,i_id):
        if i_id == '0':
            form = ShopBannerInfoForm(request.POST,request.FILES)
        else:
            qs_banner_info = ShopBannerInfo.objects.get(pk=i_id)
            form = ShopBannerInfoForm(request.POST,request.FILES,instance=qs_banner_info)

        res = {}
        if form.is_valid():
            try:
                form.save()
                res['status'] = 0
            except Exception as e:
                print(e)
                res['status'] = 1

        return render(request, 'shop/banner_info_edit.html', locals())




