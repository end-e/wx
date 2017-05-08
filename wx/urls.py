# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import xadmin
from xadmin.plugins import xversion
# from wxaccess.views import WeChatAccessView, GetAccessTokenView
xadmin.autodiscover()

xversion.register_models()

urlpatterns = [
    url(r'xadmin/', include(xadmin.site.urls)),
    # 微信接入url (wx.huigo.com)
    url(r'^/$', 'api.views.conn', name='check_signature'),
    # api
    url(r'^api/', include('api.urls', namespace='api')),
]
