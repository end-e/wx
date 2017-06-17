# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from admin.views.sys.website import LoginView, LogoutView, ResetPwdView, IndexView, CodeView
from admin.views.sys.user import UserEditView, UserView, UserInfoView, UserAddView
from admin.views.sys.role import RoleEditView, RoleView, RoleAddView, RoleNavView
from admin.views.sys.nav import NavEditView, NavView, NavAddView

urlpatterns = [
    # 会员绑定页面
    url(r'^$', IndexView.as_view(), name='index'),
    # 登陆相关
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^vcode/$', CodeView.as_view(), name='vcode'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^reset/$', ResetPwdView.as_view(), name='reset'),

    url(r'^user/$', UserView.as_view(), name='user'),
    url(r'^user/edit/(?P<user_id>\d+$)', UserEditView.as_view(), name='user_edit'),
    url(r'^user/add/', UserAddView.as_view(), name='user_add'),
    url(r'^user/info/(?P<user_id>\d+$)', UserInfoView.as_view(), name='user_info'),

    url(r'^role/$', RoleView.as_view(), name='role'),
    url(r'^role/edit/(?P<role_id>\d+$)', RoleEditView.as_view(), name='role_edit'),
    url(r'^role/add/', RoleAddView.as_view(), name='role_add'),
    url(r'^role/nav/(?P<role_id>\d+$)', RoleNavView.as_view(), name='role_nav'),

    url(r'^nav/$', NavView.as_view(), name='nav'),
    url(r'^nav/edit/(?P<nav_id>\d+$)', NavEditView.as_view(), name='nav_edit'),
    url(r'^nav/add/', NavAddView.as_view(), name='nav_add'),

    url(r'^giftcard/', include('admin.views.giftcard.urls', namespace='giftcard'))

]
