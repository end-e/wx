# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()

xversion.register_models()
import os
root_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    url(r'xadmin/', include(xadmin.site.urls)),
    # 微信文件校验地址
    url(r'MP_verify_QthEcNlYA73MNXgH.txt', 'api.views.views.verify', name='MP_verify_QthEcNlYA73MNXgH.txt'),

    # 微信接入url (www.zisai.net)
    url(r'^$', 'api.views.views.conn', name='check_signature'),
    # api
    url(r'^api/', include('api.urls', namespace='api')),
    #admin
    url(r'^admin/', include('admin.urls', namespace='admin')),
    # 会员微信绑定模块
    url(r'^user/', include('user.urls', namespace='user')),

    url(r'^collected_static/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': root_path+'/collected_static/css'}),
    url(r'^collected_static/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': root_path+'/collected_static/js'}),
    url(r'^collected_static/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':root_path+ '/collected_static/img'}),
    url(r'^collected_static/font/(?P<path>.*)$', 'django.views.static.serve', {'document_root':root_path+ '/collected_static/font'}),
    url(r'^collected_static/ico/(?P<path>.*)$', 'django.views.static.serve', {'document_root':root_path+ '/collected_static/ico'}),
    url(r'^collected_static/wx/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':root_path+ '/collected_static/wx/js'}),
]
