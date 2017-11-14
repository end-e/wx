# -*- coding: utf-8 -*-
from django import forms
from cash_coupons.models import CashCoupon


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    img = forms.FileField()


class CashCouponsAddForm(forms.ModelForm):
    class Meta:
        model = CashCoupon
        fields =['code_type','brand_name','title','color','notice','description',
                 'begin_time','end_time','least_cost','reduce_cost']


