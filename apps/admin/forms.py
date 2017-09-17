# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 11:27'
from django import forms

from admin.models import User,Nav,Role,GiftCard,ShopTheme,ShopGood,ShopCategory,ShopBanner,ShopBannerInfo,\
    GiftOrderRefund

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
                  'price','brand_name','quantity','max_give',
                  'notice','description','wx_card_id']


class GiftCardEditForm(forms.ModelForm):
    action = forms.CharField(required=True)
    class Meta:
        model = GiftCard
        fields = ['name','logo','notice','description','wx_card_id']


class ShopGoodForm(forms.ModelForm):
    class Meta:
        model = ShopGood
        fields = ['name','sn','price','img','category','stock','is_hot','is_new','status']


class ShopThemeForm(forms.ModelForm):
    class Meta:
        model = ShopTheme
        fields = ['name','desc','img','banner','begin_time','end_time','sort']


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

class GiftRefundForm(forms.ModelForm):
    class Meta:
        model = GiftOrderRefund
        fields = ['trans_id','tel','number','wx']