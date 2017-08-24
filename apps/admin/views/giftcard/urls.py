# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/14 10:26'
from django.conf.urls import url

from admin.views.giftcard.base import ImgUploadView,ImgView,ThemeView,ImgDelView,ThemeEditView,ImgStatusView
from admin.views.giftcard.card import CardEditView,CardView,CardWxView,CardDelView,CardInfoWxView, \
    CardUpCodeManualView,CardModifyStockView,CheckCodeInfo,CardStockView,ChangBalanceView
from admin.views.giftcard.page import UploadPageView,PageView
from admin.views.giftcard.report import OrderView,BizuininfoView,CardPaidView

urlpatterns = [
    #图片素材
    url(r'^img/edit/$',ImgUploadView.as_view(),name='img_upload'),
    url(r'^img/(?P<page_id>[0-9]+)$',ImgView.as_view(),name='imgs'),
    url(r'^img/del/',ImgDelView.as_view(),name='img_del'),
    url(r'^img/status/(?P<img_id>[0-9]+)/(?P<status>[0-9])$', ImgStatusView.as_view(), name='img_status'),


    #基础主题
    url(r'^theme/$',ThemeView.as_view(),name='themes'),
    url(r'^theme/edit/(?P<theme_id>[0-9]+)/(?P<step_id>[0-9])$',ThemeEditView.as_view(),name='theme_edit'),
    url(r'^theme/item/del$','admin.views.giftcard.base.themeItemDel',name='theme_item_del'),
    #货架
    url(r'^page/$', PageView.as_view(), name='page'),
    url(r'^page/edit/(?P<page_id>[\S]+)/$',UploadPageView.as_view(),name='page_edit'),
    #card
    url(r'^card/$',CardView.as_view(),name='cards'),
    url(r'^card/edit/(?P<card_id>[0-9]+)/$',CardEditView.as_view(),name='card_edit'),
    url(r'^card/del/$',CardDelView.as_view(),name='card_del'),
    url(r'^card/wx/(?P<page_num>[0-9]+)/$',CardWxView.as_view(),name='cards_wx'),
    url(r'^card/wx/info/(?P<wx_card_id>[\S]+)$',CardInfoWxView.as_view(),name='card_wx'),
    url(r'^card/code/upload/manual/(?P<wx_card_id>[\S]+)',CardUpCodeManualView.as_view(),name='card_code_upload_manual'),
    url(r'^card/code/get/','admin.utils.method.getCardCode2',name='card_code_get_guest'),
    url(r'^card/stock/$',CardStockView.as_view(),name='card_stock'),
    url(r'^card/stock/modify/$',CardModifyStockView.as_view(),name='card_stock_modify'),
    url(r'^card/check/code/wx/(?P<card_id>[\S]+)/(?P<code>[0-9]+)$',CheckCodeInfo.as_view(),name='card_check_code_wx'),
    url(r'^card/change/balance/(?P<card_id>[\S]+)/(?P<code>[0-9]+)/(?P<balance>.*)',ChangBalanceView.as_view()),


    #Report
    url(r'^order/$',OrderView.as_view(),name='orders'),
    url(r'^bizuininfo/$',BizuininfoView.as_view(),name='bizuininfo'),
    url(r'^paid/$',CardPaidView.as_view(),name='card_paid'),

]