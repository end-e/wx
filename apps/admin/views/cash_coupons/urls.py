# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CashCouponsStoreListView, CashCouponsImgListView, CashCouponsImgUploadView

urlpatterns = [
    # 门店列表
    url(r'^store/list/$', CashCouponsStoreListView.as_view(), name='store_list'),
    # 素材模块
    url(r'^img/list/$', CashCouponsImgListView.as_view(), name='img_list'),
    url(r'^img/edit/', CashCouponsImgUploadView.as_view(), name='img_edit'),
    # 代金券模块
    # url(r'^coupons/list/$', CashCouponsListView.as_view(), name='cash_coupons_list'),
]
