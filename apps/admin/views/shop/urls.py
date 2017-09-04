# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/7/24 15:29'
from django.conf.urls import url

from admin.views.shop.good import GoodView,GoodEditView,GoodCategoryView,GoodImgEditView,GoodPropertyEditView
from admin.views.shop.category import CategoryView,CategoryEditView
from admin.views.shop.theme import ThemeView,ThemeEditView,ThemeInfoEditView
from admin.views.shop.banner import BannerView,BannerEditView,BannerInfoView,BannerInfoEditView
from admin.views.shop.order import OrderView

urlpatterns = [
    url(r'^good/$',GoodView.as_view(),name='goods'),
    url(r'^good/edit/(?P<good_id>[0-9]+)/$',GoodEditView.as_view(),name='good_edit'),
    url(r'^good/img/edit/(?P<good_sn>[0-9]+)/$',GoodImgEditView.as_view(),name='good_img_edit'),
    url(r'^good/property/edit/(?P<good_sn>[0-9]+)/$',GoodPropertyEditView.as_view(),name='good_property_edit'),
    url(r'^good/cate/$',GoodCategoryView.as_view(),name='good_category'),

    url(r'^category/$',CategoryView.as_view(),name='category'),
    url(r'^category/edit/(?P<c_id>[0-9]+)/$',CategoryEditView.as_view(),name='category_edit'),

    url(r'^theme/$',ThemeView.as_view(),name='theme'),
    url(r'^theme/edit/(?P<t_id>[0-9]+)/$',ThemeEditView.as_view(),name='theme_edit'),
    url(r'^theme/info/edit/(?P<t_id>[0-9]+)/$',ThemeInfoEditView.as_view(),name='theme_info_edit'),

    url(r'^banner/$',BannerView.as_view(),name='banner'),
    url(r'^banner/edit/(?P<b_id>[0-9]+)/$',BannerEditView.as_view(),name='banner_edit'),
    url(r'^banner/info/(?P<b_id>[0-9]+)/$',BannerInfoView.as_view(),name='banner_info'),
    url(r'^banner/info/edit/(?P<b_id>[0-9]+)/(?P<i_id>[0-9]+)$',BannerInfoEditView.as_view(),name='banner_info_edit'),

    url(r'^order/(?P<page>[0-9]+)/$',OrderView.as_view(),name='orders'),
]


