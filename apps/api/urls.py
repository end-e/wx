# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/18 15:02'
from django.conf.urls import url
from . import views, cron

urlpatterns = [
    url(r'^hx/(?P<sn>.*)/(?P<stamp>\d+)', views.hx, name='hx'),
    url(r'cron/token/', cron.cron_get_token(), name='cron_get_token'),
    url(r'cron/temp/', cron.cron_send_temp, name='cron_send_temp'),
]
