# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CashCouponsStoreListView, CashCouponsImgListView, CashCouponsImgUploadView, \
    CashCouponsImgDetailView, CashCouponsImgStatusView

urlpatterns = [
    # 门店列表
    url(r'^store/list/$', CashCouponsStoreListView.as_view(), name='store_list'),
    # 素材模块
    url(r'^img/list/$', CashCouponsImgListView.as_view(), name='img_list'),
    url(r'^img/add/', CashCouponsImgUploadView.as_view(), name='img_add'),
    url(r'^img/detail/(?P<img_id>\d+)$', CashCouponsImgDetailView.as_view(), name='img_detail'),
    url(r'^img/status/(?P<status>[01])/(?P<img_id>\d+)', CashCouponsImgStatusView.as_view(), name='img_status'),
    # 代金券模块
    # url(r'^coupons/list/$', CashCouponsListView.as_view(), name='cash_coupons_list'),
]
