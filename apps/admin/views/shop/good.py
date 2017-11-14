# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/24 15:29'
import json,math

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from admin.models import ShopGood,ShopCategory,ShopGoodImg,ShopGoodProperty
from admin.views.shop.forms import ShopGoodForm
from admin.utils.paginator import MyPaginator

class GoodView(View):
    def get(self,request):
        good_list = ShopGood.objects.values().all()
        page_count = 10
        total_page = math.ceil(good_list.count()/page_count)
        page = request.GET.get('page',1)
        paginator = MyPaginator(good_list, page_count)
        good_list = paginator.page(page)

        return render(request,'shop/good_list.html',locals())


class GoodEditView(View):
    def get(self,request,good_id):
        category_list = ShopCategory.objects.values('id','name').filter(status=0)
        if good_id!='0':
            good = ShopGood.objects.filter(id=good_id).first()
        return render(request,'shop/good_edit.html',locals())

    def post(self,request,good_id):
        if good_id=='0':
            form = ShopGoodForm(request.POST,request.FILES)
        else:
            qs_good = ShopGood.objects.get(pk=good_id)
            form = ShopGoodForm(request.POST,request.FILES,instance=qs_good)
        res = {}
        if form.is_valid():
            res['status'] = 0
            try:
                form.save()
            except Exception as e:
                print(e)
                res['status'] = 1

        return render(request, 'shop/good_edit.html', locals())


class GoodImgEditView(View):
    def get(self,request,good_sn):
        if good_sn=='0' :
            return redirect(reverse('admin:shop:good'))
        img_list = ShopGoodImg.objects.values('id','img','sort').filter(good_sn=good_sn)
        return render(request,'shop/good_img.html',locals())

    def post(self,request,good_sn):
        id_list = request.POST.getlist('id[]',[])
        img_list = request.FILES.getlist('img[]',[])
        sort_list = request.POST.getlist('sort[]',[])

        qs_imgs = ShopGoodImg.objects.values('id').filter(good_sn=good_sn)
        qs_img_ids = [img['id'] for img in qs_imgs]

        remove_list = [id for id in qs_img_ids if str(id) not in id_list]
        res = {}
        try:
            ShopGoodImg.objects.filter(id__in=remove_list).delete()
            good_img_list = []
            for i in range(0,len(img_list)):
                if len(id_list) > 0 and id_list[i]:
                    qs_img = ShopGoodImg.objects.get(id=id_list[i])
                    qs_img.img=img_list[i]
                    qs_img.sort=sort_list[i]
                    qs_img.save()
                else:
                    good_img = ShopGoodImg()
                    good_img.img = img_list[i]
                    good_img.sort = sort_list[i]
                    good_img.good_sn = good_sn
                    good_img_list.append(good_img)
            ShopGoodImg.objects.bulk_create(good_img_list)
            res['status'] = 0
        except Exception as e:
            print(e)
            res['status'] = 1

        return render(request, 'shop/good_img.html', locals())


class GoodPropertyEditView(View):
    def get(self,request,good_sn):
        if good_sn=='0' :
            return redirect(reverse('admin:shop:good'))
        property_list = ShopGoodProperty.objects.values('id','name','detail','sort').filter(good_sn=good_sn)
        return render(request,'shop/good_property.html',locals())


    def post(self,request,good_sn):
        id_list = request.POST.getlist('id[]',[])
        name_list = request.POST.getlist('name[]',[])
        detail_list = request.POST.getlist('detail[]',[])
        sort_list = request.POST.getlist('sort[]',[])

        qs_properties = ShopGoodProperty.objects.values('id').filter(good_sn=good_sn)
        qs_property_ids = [property['id'] for property in qs_properties]

        remove_list = [id for id in qs_property_ids if str(id) not in id_list]
        res = {}
        try:
            ShopGoodProperty.objects.filter(id__in=remove_list).delete()
            good_property_list = []
            for i in range(0,len(name_list)):
                if len(id_list) > 0 and id_list[i]:
                    qs_property = ShopGoodProperty.objects.filter(id=id_list[i])\
                        .update(name=name_list[i],detail=detail_list[i],sort=sort_list[i])
                else:
                    good_property = ShopGoodProperty()
                    good_property.name = name_list[i]
                    good_property.detail = detail_list[i]
                    good_property.sort = sort_list[i]
                    good_property.good_sn = good_sn
                    good_property_list.append(good_property)
            ShopGoodProperty.objects.bulk_create(good_property_list)
            res['status'] = 0
        except Exception as e:
            print(e)
            res['status'] = 1

        return render(request, 'shop/good_img.html', locals())


class GoodCategoryView(View):
    def get(self,request):
        c_id = request.GET.get('id','')
        res = {'status':0}
        try:
            good_list = ShopGood.objects.values('sn','name').filter(category=c_id)
            res['data'] = list(good_list)
        except Exception as e:
            res['status'] = 1
            print(e)
        return HttpResponse(json.dumps(res))

