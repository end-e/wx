# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/4/18 15:02'
from django.conf.urls import url
from . import views,cron


urlpatterns = [
    url(r'^conn/',views.conn,name='conn'),
    url(r'^hx/(?P<sn>.*)/(?P<stamp>\d+)',views.hx,name='hx'),
    url(r'msgTemplate/get/',views.get_template_id,name='get_template_id'),
    url(r'cron/temp/',cron.cron_send_temp,name='cron_send_temp'),
]
