# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import voucher, poster

urlpatterns = [
    #券操作页面
    url(r'^voucher/index/$', voucher.index, name="voucher_index"),
    url(r'^voucher/edit/(?P<voucher_id>[0-9]+)$', voucher.voucherEdit, name='voucher_edit'),
    url(r'^voucher/save/$', voucher.voucherSave, name="voucher_save"),
    #海报操作
    url(r'^poster/index/$', poster.index, name="poster_index"),
    url(r'^poster/edit/(?P<poster_id>[0-9]+)$', poster.posterEdit, name='poster_edit'),
    url(r'^poster/save/$', poster.posterSave, name="poster_save"),
]