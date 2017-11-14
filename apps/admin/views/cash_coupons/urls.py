# -*- coding: utf-8 -*-
from django.conf.urls import url

from .coupon import CouponsStoreListView, CouponsAddView,CouponsListView
from .img import  CouponsImgListView, CouponsImgUploadView,CouponsImgDetailView, CouponsImgStatusView

urlpatterns = [
    # 门店列表
    url(r'^store/list/$', CouponsStoreListView.as_view(), name='store_list'),
    # 素材模块
    url(r'^img/list/$', CouponsImgListView.as_view(), name='img_list'),
    url(r'^img/add/', CouponsImgUploadView.as_view(), name='img_add'),
    url(r'^img/detail/(?P<img_id>\d+)$', CouponsImgDetailView.as_view(), name='img_detail'),
    url(r'^img/status/(?P<status>[01])/(?P<img_id>\d+)', CouponsImgStatusView.as_view(), name='img_status'),
    # 代金券模块
    url(r'^coupons/list/$', CouponsListView.as_view(), name='coupons'),
    url(r'^coupons/add/$', CouponsAddView.as_view(), name='add'),
    # url(r'^coupons/info/sql/$', 'utils.data.getCouponInfo', name='info'),
    url(r'^coupons/info/mssql/$', 'utils.data.getCouponInfo', name='info2'),
]
