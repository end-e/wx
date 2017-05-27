# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/26 13:44'
import json

from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse

from admin.models import Nav
from admin.forms import NavForm
from admin.utils import method
from admin.utils.paginator import MyPaginator


class NavView(View):
    def get(self,request):
        nav_list = Nav.objects.values('id', 'name', 'url','parent', 'sort','status','icon')\
            .filter(status='0')

        return render(request, 'sys/nav.html', locals())



class NavEditView(View):
    def get(self,request,nav_id):
        nav = Nav.objects.values('name', 'url','parent','sort','status','icon')\
            .filter(id=nav_id).first()
        return render(request,'sys/nav_edit.html',locals())
    def post(self,request,nav_id):
        msg = {}
        try:
            nav = Nav.objects.get(pk=nav_id)
            form = NavForm(request.POST.copy(),instance=nav)
            if form.is_valid():
                result = form.save()
                if result:
                    msg['status'] = 0
                else:
                    msg['status'] = 1
            else:
                msg['status'] = 1
        except:
            msg['status'] = 1
        return render(request, 'sys/nav_edit.html', locals())


class NavAddView(View):
    def get(self,request):
        return render(request,'sys/nav_add.html')
    def post(self,request):
        form = NavForm(request.POST)
        msg = {}
        if form.is_valid():
            result = form.save()
            if result:
                msg['status'] = 0
            else:
                msg['status'] = 1
        else:
            msg['status'] = 1
        return render(request, 'sys/nav_add.html', locals())
