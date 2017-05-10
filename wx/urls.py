# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()

xversion.register_models()

urlpatterns = [
    url(r'xadmin/', include(xadmin.site.urls)),
    # 微信接入url (www.zisai.net)
    url(r'^$', 'api.views.conn', name='check_signature'),

    # api
    url(r'^api/', include('api.urls', namespace='api')),

    # 会员微信绑定模块
    url(r'^user/', include('user.urls', namespace='user')),
]
