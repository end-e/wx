# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 8:57'
from django.shortcuts import render
from django.views.generic.base import View

from admin.forms import UserForm
from admin.models import User
from admin.utils import method

class UserEditView(View):
    def get(self, request, user_id):
        user_id = user_id
        if(user_id):
            user = User.objects.values('nick','name','pwd','role','status').filter(id=user_id).first()
        return render(request, 'base/user_edit.html', locals())

    def post(self, request, user_id):
        form = UserForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            pwd = request.POST.get('pwd', '')
            pwd = method.md5('ikg'+pwd)
            nick = request.POST.get('nick', '')
            role = request.POST.get('role', '')
            status = request.POST.get('status', '')
            if user_id:
                result = User.objects.filter(id=user_id).update(name=name, pwd=pwd, nick=nick, role=role, status=status)
            else:
                result = User.objects.create(name=name, pwd=pwd, nick=nick, role=role, status=status)
            msg = {}
            if result:
                msg['status'] = 0
            else:
                msg['status'] = 1
        return render(request, 'base/user_edit.html', locals())
