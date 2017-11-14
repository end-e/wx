# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/24 15:29'
from django.shortcuts import render
from django.views.generic.base import View

from admin.models import ShopCategory
from admin.views.shop.forms import ShopCategoryForm

class CategoryView(View):
    def get(self,request):
        category_list = ShopCategory.objects.values('id','name','parent','sort','status').all()
        return render(request,'shop/category_list.html',locals())


class CategoryEditView(View):
    def get(self,request,c_id):
        if c_id!='0':
            category = ShopCategory.objects.values('name','parent','sort','status','banner').filter(id=c_id).first()
        return render(request,'shop/category_edit.html',locals())

    def post(self,request,c_id):
        if c_id=='0':
            form = ShopCategoryForm(request.POST,request.FILES)
        else:
            qs_category = ShopCategory.objects.get(pk=c_id)
            form = ShopCategoryForm(request.POST,request.FILES,instance=qs_category)

        res = {}
        if form.is_valid():
            res['status'] = 0
            try:
                form.save()
            except Exception as e:
                print(e)
                res['status']=1
        return render(request,'shop/category_edit.html',locals())


