# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import voucher, poster, product
from .voucher import DiscodeListViews, DiscodeQueryViews, AddDiscodeViews

urlpatterns = [
    # 券操作页面
    url(r'^voucher/index/$', voucher.index, name="voucher_index"),
    url(r'^voucher/edit/(?P<voucher_id>[0-9]+)$', voucher.voucherEdit, name='voucher_edit'),
    url(r'^voucher/delete/(?P<voucher_id>[0-9]+)$', voucher.voucherDelete, name='voucher_delete'),
    url(r'^voucher/save/$', voucher.voucherSave, name="voucher_save"),
    url(r'^voucher/class_list/$', voucher.classList, name="class_list"),
    url(r'^voucher/class_edit/(?P<class_id>[0-9]+)$', voucher.classEdit, name='class_edit'),
    url(r'^voucher/class_delete/(?P<class_id>[0-9]+)$', voucher.classDelete, name='class_delete'),
    url(r'^voucher/class_save/$', voucher.classSave, name="class_save"),
    # 海报操作
    url(r'^poster/index/$', poster.index, name="poster_index"),
    url(r'^poster/edit/(?P<poster_id>[0-9]+)$', poster.posterEdit, name='poster_edit'),
    url(r'^poster/delete/(?P<poster_id>[0-9]+)$', poster.posterDelete, name='poster_delete'),
    url(r'^poster/save/$', poster.posterSave, name="poster_save"),
    # 商品信息维护
    url(r'^product/index/$', product.index, name="product_index"),
    url(r'^product/edit/(?P<product_id>[0-9]+)$', product.productEdit, name='product_edit'),
    url(r'^product/delete/(?P<product_id>[0-9]+)$', product.productDelete, name='product_delete'),
    url(r'^product/save/$', product.productSave, name="product_save"),
    # 券验证码管理
    url(r'^discode/$', DiscodeListViews.as_view(), name='discode_list'),
    url(r'^discode/query/', DiscodeQueryViews.as_view(), name='discode_query'),
    url(r'^discode/create/', AddDiscodeViews.as_view(), name='discode_create'),
]
