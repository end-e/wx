# -*- coding: utf-8 -*-
import os

from django.conf.urls import include, url
from django.views.static import serve
# import xadmin
# from xadmin.plugins import xversion

from wx.settings import MEDIA_ROOT

# xadmin.autodiscover()

# xversion.register_models()

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    # url(r'xadmin/', include(xadmin.site.urls)),
    # 微信文件校验地址
    url(r'MP_verify_QthEcNlYA73MNXgH.txt', 'api.views.views.verify', name='MP_verify_QthEcNlYA73MNXgH.txt'),
    # CA证书校验地址
    url(r'.well-known/pki-validation/fileauth.txt', 'api.views.views.ca',
        name='.well-known/pki-validation/fileauth.txt'),

    # 微信接入url (www.zisai.net)
    url(r'^$', 'api.views.views.conn', name='check_signature'),
    # api
    url(r'^api/', include('api.urls', namespace='api')),
    # admin
    url(r'^admin/', include('admin.urls', namespace='admin')),
    # 会员微信绑定模块
    url(r'^user/', include('user.urls', namespace='user')),
    # 微信后台
    url(r'^wxapp/', include('admin.views.wxapp.urls', namespace='wxapp')),
    # 微信接口
    url(r'^wxapp/', include('api.views.wxapp.urls', namespace='wxapp')),

    url(r'^collected_static/css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/css'}),
    url(r'^collected_static/js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/js'}),
    url(r'^collected_static/img/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/img'}),
    url(r'^collected_static/font/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/font'}),
    url(r'^collected_static/ico/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/ico'}),
    url(r'^collected_static/wx/js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/collected_static/wx/js'}),
    url(r'^common_static/wx/js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': root_path + '/common_static/wx/js'}),

    # 微信小程序图片
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    # 微信礼品卡
    url(r'^giftcard/$', include('giftcard.urls', namespace='giftcard')),


    url(r'^user/point/(?P<member_id>.*)/(?P<card_no>.*)/(?P<total_pay>.*)/(?P<result_point>.*)/$', 'utils.shop.updateGuestPoint', ),
    url(r'^guest/orders/$', 'utils.data.get_user_order1', ),
]
