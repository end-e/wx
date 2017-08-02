# -*-  coding:utf-8 -*-
# __author__ = ''
# __date__ = '2017/4/18 15:02'
from django.conf.urls import url,include

from api.views import views, cron, sms,pay,shop

urlpatterns = [
    # 微信后台配置的url
    url(r'^checksignature/$', views.conn, name='checksignature'),
    url(r'conn/', views.conn, name='conn'),
    url(r'cron/token/ikg', cron.cron_get_ikg_token, name='cron_get_ikg_token'),
    url(r'cron/token/kgcs', cron.cron_get_kgcs_token, name='cron_get_kgcs_token'),
    url(r'cron/temp/', cron.cron_send_temp, name='cron_send_temp'),
    url(r'cron/gift/card/check', cron.cron_gift_compare_order, name='cron_gift_card_check'),
    url(r'cron/gift/change/balance/$', cron.cron_gift_change_balance, name='cron_gift_change_balance'),
    url(r'cron/gift/change/balance2/$', cron.cron_gift_change_balance2, name='cron_gift_change_balance2'),

    # 配置自定义菜单(https://www.zisai.net/api/menu/create/)
    url(r'^menu/create/$', views.create_nav, name='menu_create'),
    url(r'^sms/$', sms.main, name='sms'),

    # 微信小程序获取用户openid，session_key接口
    url(r'xcx/getopenid', views.get_session_key, name='getopenid'),

    url(r'^wxapp/',include('api.views.wxapp.urls',namespace='jf')),

    #积分商城
    url(r'^shop/banner/(?P<b_id>[0-9]+)/$',shop.getBanner),
    url(r'^shop/themes/$',shop.getThemes),
    url(r'^shop/theme/(?P<t_id>[0-9]+)/$',shop.getTheme),

    url(r'^shop/good/new/$',shop.getGoodNew),
    url(r'^shop/good/(?P<g_sn>[0-9]+)/$',shop.getGood),

    url(r'^shop/category/all/$',shop.getCategories),
    url(r'^shop/category/info/(?P<c_id>[0-9]+)/$',shop.getCategoryInfo),

    url(r'^shop/user/save/$',shop.userSave),
    url(r'^shop/user/addresses/(?P<openid>[\S]+)$',shop.getUserAddresses),
    url(r'^shop/user/address/edit/(?P<openid>[\S]+)$',shop.userAddressEdit),
    url(r'^shop/user/orders/(?P<openid>[\S]+)/(?P<page>[0-9]+)$',shop.getUserOrders),
    url(r'^shop/user/order/save/$',shop.userOrderEdit),
    url(r'^shop/order/(?P<sn>[0-9]+)/$',shop.getOrder),

    #微信支付
    url(r'^wx/pay/prepay/$', pay.getPay),
    url(r'^wx/pay/notify/$', pay.payNotify),


]
