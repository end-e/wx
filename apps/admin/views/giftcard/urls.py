# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/14 10:26'
from django.conf.urls import url

from admin.views.giftcard.base import UploadImgView,UploadImgView2,ImgView,CategoryView,CategoryEditView,\
    ThemeView,ThemeEditView
from admin.views.giftcard.card import CardEditView,CardView,CardWxView,CardDelView,CardInfoWxView
from admin.views.giftcard.page import CreatePageView,UploadPageView,PageView
from admin.views.giftcard.order import OrderView

urlpatterns = [
    #图片素材
    url(r'^upload/img/$',UploadImgView.as_view(),name='upload_img'),
    url(r'^upload/img2',UploadImgView2.as_view(),name='upload_img2'),
    url(r'^img/$',ImgView.as_view(),name='imgs'),
    #基础分类
    url(r'^category/$',CategoryView.as_view(),name='categorys'),
    url(r'^category/edit/(?P<category_id>[0-9]+)$',CategoryEditView.as_view(),name='category_edit'),
    #基础主题
    url(r'^theme/$',ThemeView.as_view(),name='themes'),
    url(r'^theme/edit/(?P<theme_id>[0-9]+)$',ThemeEditView.as_view(),name='theme_edit'),
    #货架
    url(r'^page/$', PageView.as_view(), name='page'),
    url(r'^page/edit/(?P<page_id>.*)/$',UploadPageView.as_view(),name='edit_page'),
    #card
    url(r'^card/$',CardView.as_view(),name='cards'),
    url(r'^card/edit/(?P<card_id>[0-9]+)/$',CardEditView.as_view(),name='card_edit'),
    url(r'^card/del/(?P<card_id>.*)/$',CardDelView.as_view(),name='card_del'),
    url(r'^card/wx/(?P<page_num>[0-9]+)/$$',CardWxView.as_view(),name='cards_wx'),
    url(r'^card/wx/info/(?P<wx_card_id>.*)$',CardInfoWxView.as_view(),name='card_wx'),
    #订单
    url(r'^order/$',OrderView.as_view(),name='orders'),
]