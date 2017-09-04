# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/9/4 13:41'
from django.conf.urls import url

from api.views.shop import order,pay,token,user,base
urlpatterns =[
    #banner
    url(r'^banner/(?P<b_id>[0-9]+)/$',base.getBannerById),

    #主题相关接口
    url(r'^themes/$',base.getThemes),
    url(r'^theme/(?P<t_id>[0-9]+)/$',base.getThemeById),

    #商品相关接口
    url(r'^good/new/$',base.getNewGood),
    url(r'^good/(?P<g_sn>[0-9]+)/$',base.getGoodBySn),

    #分类相关接口
    url(r'^category/all/$',base.getCategories),
    url(r'^category/info/(?P<c_id>[0-9]+)/$',base.getCategoryById),

    #用户相关接口
    url(r'^user/info/$',user.getuserInfo),
    url(r'^user/save/$',user.userSave),
    url(r'^user/addresses/$',user.getUserAddresses),
    url(r'^user/address/edit/$',user.userAddressEdit),
    url(r'^user/kgmoney/$',user.getUserKgMoney),
    url(r'^user/point/$',user.getUserPoint),


    #订单相关接口
    url(r'^order/goods/save/$',order.orderGoodsSave),
    url(r'^order/kgmoney/save/$',order.orderKgMoneySave),
    url(r'^order/$',order.getOrderBySn),
    url(r'^user/orders/(?P<page>[0-9]+)$',order.getOrdersByUser),

    #微信支付相关接口
    url(r'^wx/pay/prepay/$', pay.getPay),
    url(r'^wx/pay/notify/$', pay.payNotify),

    #令牌相关接口
    url(r'^token/user/$',token.getToken),
    url(r'^token/verify/$',token.verify),

]