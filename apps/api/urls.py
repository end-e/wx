# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/18 15:02'
from django.conf.urls import url,include

from api.views import views, cron, sms

urlpatterns = [
    # 微信后台配置的url
    url(r'^checksignature/$', views.conn, name='checksignature'),
    url(r'conn/', views.conn, name='conn'),
    #定时任务相关
    url(r'cron/token/ikg', cron.cron_get_ikg_token, name='cron_get_ikg_token'),
    url(r'cron/token/kgcs', cron.cron_get_kgcs_token, name='cron_get_kgcs_token'),
    url(r'cron/temp/', cron.cron_send_temp, name='cron_send_temp'),

    url(r'cron/gift/card/check', cron.cron_gift_compare_order, name='cron_gift_card_check'),
    url(r'cron/gift/change/balance/$', cron.cron_gift_change_balance, name='cron_gift_change_balance'),
    url(r'cron/shop/order/update$', cron.cron_shop_order_sign),

    # 配置自定义菜单(https://www.zisai.net/api/menu/create/)
    url(r'^menu/create/$', views.create_nav, name='menu_create'),
    url(r'^sms/$', sms.main, name='sms'),
    # 微信小程序获取用户openid，session_key接口
    url(r'xcx/getopenid', views.get_session_key, name='getopenid'),

    url(r'^wxapp/',include('api.views.wxapp.urls',namespace='jf')),

    url(r'^shop/', include('api.views.shop.urls', namespace='shop')),
]
