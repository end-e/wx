# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import voucher, member, poster

urlpatterns = [
    # 会员绑定页面
    url(r'^member/getInfo/$', member.getInfo, name="member_getInfo"),
    #券操作页面
    url(r'^voucher/getList/$', voucher.getVoucherList, name="voucher_getList"),
    url(r'^voucher/getInfo/$', voucher.getVoucherInfo, name="voucher_getInfo"),
    #海报操作
    url(r'^poster/getList/$', poster.getPosterList, name="poster_getList"),
    url(r'^poster/getInfo/$', poster.getPosterInfo, name="poster_getInfo"),

]