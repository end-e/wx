# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 11:27'
from django import forms

from admin.models import User,Nav,Role,GiftCard,ShopTheme,ShopGood,ShopCategory,ShopBanner,ShopBannerInfo,\
    GiftOrderRefund


class ShopGoodForm(forms.ModelForm):
    class Meta:
        model = ShopGood
        fields = ['name','sn','price','img','category','stock','is_hot','is_new','status']


class ShopThemeForm(forms.ModelForm):
    class Meta:
        model = ShopTheme
        fields = ['name','desc','img','banner','begin_time','end_time','sort','status','type']


class ShopCategoryForm(forms.ModelForm):
    class Meta:
        model = ShopCategory
        fields = ['name','parent','status','sort','banner']


class ShopBannerForm(forms.ModelForm):
    class Meta:
        model = ShopBanner
        fields = ['name','desc','status']


class ShopBannerInfoForm(forms.ModelForm):
    class Meta:
        model = ShopBannerInfo
        fields = ['name','banner','img','type','target_id','begin_time','end_time','sort']
