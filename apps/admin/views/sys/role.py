# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/26 13:44'
import json

from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse

from admin.models import Role,RoleNav,Nav
from admin.forms import RoleForm
from admin.utils import method
from admin.utils.paginator import MyPaginator


class RoleView(View):
    def get(self,request):
        roles = Role.objects.values('id', 'name', 'status')
        paginator = MyPaginator(roles, 1)
        page_num = request.GET.get('page', 1)
        try:
            roles = paginator.page(page_num)
        except Exception as e:
            print(e)
        return render(request, 'sys/role.html', locals())



class RoleEditView(View):
    def get(self,request,role_id):
        role = Role.objects.values('id','name','status').filter(id=role_id).first()
        return render(request,'sys/role_edit.html',locals())
    def post(self,request,role_id):
        msg = {}
        try:
            role = Role.objects.get(pk=role_id)
            form = RoleForm(request.POST, instance=role)
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

        return render(request, 'sys/role_edit.html', locals())


class RoleAddView(View):
    def get(self,request):
        return render(request,'sys/role_add.html')
    def post(self,request):
        form = RoleForm(request.POST)
        msg = {}
        if form.is_valid():
            result = form.save()
            if result:
                msg['status'] = 0
            else:
                msg['status'] = 1
        else:
            msg['status'] = 1
        return render(request, 'sys/role_add.html', locals())


class RoleNavView(View):
    def get(self,request,role_id):
        data = {}
        my_nav = method.getUserNav(role_id=str(role_id))
        my_nav_list = method.createNavList(my_nav)

        navData = Nav.objects.values('id','name','parent','sort').filter(status='0')
        navList = method.createNavList(navData)

        return render(request,'sys/role_nav.html',locals())
    def post(self,request,role_id):
        menu_list = request.POST.get('menu_list','')
        menu_list = menu_list.split(',')
        action = request.POST.get('action')
        msg = {}
        if action == 'delete':
            try:
                RoleNav.objects.filter(role=role_id,nav_id__in=menu_list).delete()
                msg['status'] = 0
            except:
                msg['status'] = 1
        elif action == 'put':
            role_nav_list = []
            for menu in menu_list:
                role_nav = RoleNav()
                role_nav.role_id = role_id
                role_nav.nav_id = menu
                role_nav_list.append(role_nav)
            try:
                RoleNav.objects.bulk_create(role_nav_list)
                msg['status'] = 0
            except Exception as e:
                print(e)
                msg['status'] = 1
        return HttpResponse(json.dumps(msg))


