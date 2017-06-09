# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import voucher, member, product, poster

urlpatterns = [
    # 会员绑定页面
    url(r'^member/getInfo/$', member.getInfo, name="member_getInfo"),
    # 券操作页面
    url(r'^voucher/getList/$', voucher.getVoucherList, name="voucher_getList"),
    url(r'^voucher/getInfo/$', voucher.getVoucherInfo, name="voucher_getInfo"),
    url(r'^voucher/getClass/$', voucher.getVoucherClass, name="voucher_getClass"),
    # 商品页面
    url(r'^product/getList/$', product.getProductList, name="product_getList"),
    url(r'^product/getInfo/$', product.getProductInfo, name="product_getInfo"),
    # 海报操作
    url(r'^poster/getList/$', poster.getPosterList, name="poster_getList"),
    url(r'^poster/getInfo/$', poster.getPosterInfo, name="poster_getInfo"),
]
