# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 11:27'
from django import forms

from admin.models import User,Nav,Role,GiftCard

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


class GiftCardForm(forms.ModelForm):
    action = forms.CharField(required=True)
    class Meta:
        model = GiftCard
        fields = ['name','title','background_pic','logo','init_balance',
                  'price','brand_name','quantity','status','max_give',
                  'notice','description','wx_card_id']

class GiftCardEditForm(forms.ModelForm):
    action = forms.CharField(required=True)
    class Meta:
        model = GiftCard
        fields = ['name','logo','notice','description','wx_card_id']
