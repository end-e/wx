# -*- coding:utf-8 -*-
from django import forms


class AddDiscodeForm(forms.Form):
    """
    生成券验证码
    """
    batch = forms.CharField(required=True, min_length=2, max_length=2)
    nums = forms.IntegerField(required=True, max_value=10000)


class FindDiscodeForm(forms.Form):
    """
    查询券验证码
    """
    batch = forms.CharField(min_length=2, max_length=2)
    dis_code = forms.CharField(required=True, min_length=6, max_length=6)
