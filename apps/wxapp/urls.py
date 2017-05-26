# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # 会员绑定页面
    url(r'^index/$', views.index, name="wxapp_index"),
]