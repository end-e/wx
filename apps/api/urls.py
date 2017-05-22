# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/18 15:02'
from django.conf.urls import url
from . import views, cron

urlpatterns = [
    # 微信后台配置的url
    url(r'^checksignature/$', views.conn, name='checksignature'),
    url(r'^hx/(?P<sn>.*)/(?P<stamp>\d+)', views.hx, name='hx'),
    url(r'conn/', views.conn, name='conn'),
    url(r'cron/token/', cron.cron_get_token, name='cron_get_token'),
    url(r'cron/temp/', cron.cron_send_temp, name='cron_send_temp'),
    url(r'^menu/create/$', views.create_nav, name='menu_create'),

    url(r'^test/$', views.test)


]
