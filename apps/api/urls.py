# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/18 15:02'
from django.conf.urls import url,include

from api.views import views, cron, sms,pay

urlpatterns = [
    # 微信后台配置的url
    url(r'^checksignature/$', views.conn, name='checksignature'),
    url(r'conn/', views.conn, name='conn'),
    url(r'cron/token/ikg', cron.cron_get_ikg_token, name='cron_get_ikg_token'),
    url(r'cron/token/kgcs', cron.cron_get_kgcs_token, name='cron_get_kgcs_token'),
    url(r'cron/temp/', cron.cron_send_temp, name='cron_send_temp'),

    url(r'^menu/create/$', views.create_nav, name='menu_create'),
    url(r'^sms/$', sms.main, name='sms'),

    # 微信小程序获取用户openid，session_key接口
    url(r'xcx/getopenid', views.get_session_key, name='getopenid'),

    url(r'^wxapp/',include('api.views.wxapp.urls',namespace='jf')),

    #微信支付
    url(r'^wx/pay/$', pay.getPay),
    url(r'^wx/pay/notify/$', pay.payNotify),

]
