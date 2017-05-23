# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 11:27'
from django import forms

from admin.models import User

class UserForm(forms.Form):
    nick = forms.CharField(required=True)
    name = forms.CharField(required=True)
    pwd = forms.CharField(required=True, min_length=6)
    class Meta:
        model = User
        fields = ['name','pwd','nick','role','status']



