# -*- coding: utf-8 -*-
from django.conf.urls import url
from giftcard import views

urlpatterns = [
    url(r'^$', views.conn, name='conn'),
]
