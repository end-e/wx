# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import xadmin
from xadmin.plugins import xversion

from apps.api import views

xadmin.autodiscover()

xversion.register_models()

urlpatterns = [
    url(r'xadmin/', include(xadmin.site.urls)),
    # 微信文件校验地址
    url(r'MP_verify_QthEcNlYA73MNXgH.txt', views.verify, name='MP_verify_QthEcNlYA73MNXgH.txt'),

    # api
    url(r'^api/', include('api.urls', namespace='api')),

    # 会员微信绑定模块
    url(r'^user/', include('user.urls', namespace='user')),
]
