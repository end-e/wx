# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import voucher, member

urlpatterns = [
    # 会员绑定页面
    url(r'^member/getInfo/$', member.getInfo, name="member_getInfo"),
    #券操作页面
    url(r'^index/$', voucher.index, name="voucher_index"),
    url(r'^voucher/edit/(?P<voucher_id>[0-9]+)$', voucher.voucherEdit, name='voucher_edit'),
    url(r'^voucher/save/$', voucher.voucherSave, name="voucher_save"),
    url(r'^voucher/getList/$', voucher.getVoucherList, name="voucher_getList"),
    url(r'^voucher/getInfo/$', voucher.getVoucherInfo, name="voucher_getInfo"),
]