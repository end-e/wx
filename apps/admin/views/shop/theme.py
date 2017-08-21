# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/24 15:29'
import json

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.db import  transaction
from django.core.urlresolvers import reverse

from admin.models import ShopTheme,ShopCategory,ShopGood,ShopThemeInfo
from admin.forms import ShopThemeForm

class ThemeView(View):
    def get(self,request):
        theme_list = ShopTheme.objects.values().all()
        return render(request,'shop/theme_list.html',locals())


class ThemeEditView(View):
    def get(self,request,t_id):
        category_list = ShopCategory.objects.values('id','name').filter(status=0)
        if t_id!='0':
            theme = ShopTheme.objects.filter(id=t_id).first()
            info_list = ShopThemeInfo.objects.values('good_sn').filter(theme_id=t_id)
        return render(request,'shop/theme_edit.html',locals())

    def post(self,request,t_id):
        if t_id=='0':
            form = ShopThemeForm(request.POST,request.FILES)
        else:
            qs_theme = ShopTheme.objects.get(pk=t_id)
            form = ShopThemeForm(request.POST,request.FILES,instance=qs_theme)
        res = {}
        if form.is_valid():
            res['status'] = 0
            try:
                res_theme = form.save()
            except Exception as e:
                print(e)
                res['status'] = 1

        return render(request, 'shop/theme_edit.html', locals())



class ThemeInfoEditView(View):
    def get(self,request,t_id):
        if t_id=='0' :
            return redirect(reverse('admin:shop:theme'))
        category_list = ShopCategory.objects.values('id','name').filter(status=0)
        info_list = ShopThemeInfo.objects.values('good_sn').filter(theme_id=t_id)
        return render(request,'shop/theme_info_edit.html',locals())

    def post(self,request,t_id):
        sources = request.POST.get('sn_list','')
        sn_list = sources.split(',')
        action = request.POST.get('action')
        res = {'status':0}
        try:
            with transaction.atomic():
                if action == 'add':
                    qs_info_list = ShopThemeInfo.objects.values('good_sn').filter(theme_id=t_id)
                    qs_sn_list = [qs_info['good_sn'] for qs_info in qs_info_list]
                    add_list = [sn for sn in sn_list if sn not in qs_sn_list]
                    info_list = []
                    for sn in add_list:
                        info = ShopThemeInfo()
                        info.good_sn = sn
                        info.theme_id = t_id
                        info_list.append(info)
                    ShopThemeInfo.objects.bulk_create(info_list)
                    res['data'] = ','.join(add_list)
                elif action == 'remove':
                    ShopThemeInfo.objects.filter(good_sn__in=sn_list).delete()
                    res['data'] = sources
        except Exception as e:
            print(e)
            res['status'] = 1
        return HttpResponse(json.dumps(res))

