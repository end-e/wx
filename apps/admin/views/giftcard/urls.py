# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/14 10:26'
from django.conf.urls import url

from admin.views.giftcard.base import ImgUploadView,ImgView,ThemeView,ThemeEditView,ImgStatusView
from admin.views.giftcard.card import CardEditView,CardView,CardWxView,CardDelView,CardInfoWxView,CardUpCodeAutoView, \
    CardUpCodeManualView,CardChangeCodeView
from admin.views.giftcard.page import UploadPageView,PageView
from admin.views.giftcard.order import OrderView

urlpatterns = [
    #图片素材
    url(r'^upload/img',ImgUploadView.as_view(),name='img_upload'),
    url(r'^img/(?P<page_id>[0-9]+)$',ImgView.as_view(),name='imgs'),
    url(r'^img/status/(?P<img_id>[0-9]+)/(?P<status>[0-9])', ImgStatusView.as_view(), name='img_status'),

    #基础主题
    url(r'^theme/$',ThemeView.as_view(),name='themes'),
    url(r'^theme/edit/(?P<theme_id>[0-9]+)/(?P<step_id>[0-9])$',ThemeEditView.as_view(),name='theme_edit'),
    #货架
    url(r'^page/$', PageView.as_view(), name='page'),
    url(r'^page/edit/(?P<page_id>.*)/$',UploadPageView.as_view(),name='page_edit'),
    #card
    url(r'^card/$',CardView.as_view(),name='cards'),
    url(r'^card/edit/(?P<card_id>[0-9]+)/$',CardEditView.as_view(),name='card_edit'),
    url(r'^card/del/(?P<action>.*)/(?P<card_id>.*)/$',CardDelView.as_view(),name='card_del'),
    url(r'^card/wx/(?P<page_num>[0-9]+)/$$',CardWxView.as_view(),name='cards_wx'),
    url(r'^card/wx/info/(?P<wx_card_id>.*)$',CardInfoWxView.as_view(),name='card_wx'),
    url(r'^card/code/upload/auto/(?P<wx_card_id>.*)',CardUpCodeAutoView.as_view(),name='card_code_upload_auto'),
    url(r'^card/code/upload/manual/(?P<wx_card_id>.*)',CardUpCodeManualView.as_view(),name='card_code_upload_manual'),
    url(r'^card/code/change/(?P<wx_card_id>.*)',CardChangeCodeView.as_view(),name='card_code_change'),

    url(r'^card/code/get/','admin.utils.method.getCardCode2',name='card_code_change'),

    #订单
    url(r'^order/$',OrderView.as_view(),name='orders'),
]