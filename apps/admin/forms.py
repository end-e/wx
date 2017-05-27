# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 11:27'
from django import forms

from admin.models import User,Nav,Role

class LoginForm(forms.Form):
    name = forms.CharField(required=True)
    pwd = forms.CharField(required=True,min_length=6)


class UserForm(forms.ModelForm):
    nick = forms.CharField(required=True)
    name = forms.CharField(required=True)
    pwd = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['name','pwd','nick','role','status']


class RoleForm(forms.ModelForm):
    name = forms.CharField(required=True)
    status = forms.CharField(required=True)
    class Meta:
        model = Role
        fields = ['name','status']


class NavForm(forms.ModelForm):
    class Meta:
        model = Nav
        fields = ['name','url','parent','sort','status','icon']

