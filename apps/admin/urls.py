# -*- coding: utf-8 -*-
from django.conf.urls import url

from admin.views.website import LoginView,LogoutView,ResetPwdView,IndexView,CodeView
from admin.views.user import UserEditView

urlpatterns = [
    # 会员绑定页面
    url(r'^index/$', IndexView.as_view(), name='index'),
    #登陆相关
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^vcode/$', CodeView.as_view(), name='vcode'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^reset/$', ResetPwdView.as_view(), name='reset'),
    url(r'^user/edit/(?P<user_id>\d+|\s*)', UserEditView.as_view(), name='user_edit'),
]