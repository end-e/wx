# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 8:57'
from django.shortcuts import render
from django.views.generic.base import View
from admin.utils.paginator import MyPaginator

from admin.forms import UserForm
from admin.models import User
from admin.utils import method


class UserView(View):
    def get(self, request):
        users = User.objects.values('id', 'nick', 'role', 'status', 'add_time')
        paginator = MyPaginator(users, 1)
        page_num = request.GET.get('page', 1)
        try:
            users = paginator.page(page_num)
        except Exception as e:
            print(e)
        return render(request, 'sys/user.html', locals())


class UserEditView(View):
    def get(self, request, user_id):
        user_id = user_id
        if (user_id):
            user = User.objects.values('nick', 'name', 'pwd', 'role', 'status').filter(id=user_id).first()
        return render(request, 'sys/user_edit.html', locals())

    def post(self, request, user_id):
        form = UserForm(request.POST)
        msg = {}
        if form.is_valid():
            name = request.POST.get('name', '')
            nick = request.POST.get('nick', '')
            role = request.POST.get('role', '')
            status = request.POST.get('status', '')
            result = User.objects.filter(id=user_id).update(name=name, nick=nick, role=role, status=status)
            if result:
                msg['status'] = 0
            else:
                msg['status'] = 1
        else:
            msg['status'] = 1
        return render(request, 'sys/user_edit.html', locals())


class UserAddView(View):
    def get(self, request):
        return render(request, 'sys/user_add.html')

    def post(self, request):
        form = UserForm(request.POST)
        msg = {}
        if form.is_valid():
            name = request.POST.get('name', '')
            nick = request.POST.get('nick', '')
            role = request.POST.get('role', '')
            status = request.POST.get('status', '')
            result = User.objects.create(name=name, nick=nick, role=role, status=status)
            if result:
                msg['status'] = 0
            else:
                msg['status'] = 1
        else:
            msg['status'] = 1
        return render(request, 'sys/user_add.html', locals())


class UserInfoView(View):
    def get(self, request,user_id):
        user = User.objects.values('id', 'nick', 'role', 'status', 'add_time','name')\
            .filter(id=user_id).first()
        return render(request, 'sys/user_info.html', locals())
