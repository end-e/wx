from django.conf.urls import include, url
# from django.contrib import admin
import xadmin
from xadmin.plugins import xversion
from wxaccess.views import WeChatAccessView, GetAccessTokenView

xadmin.autodiscover()

xversion.register_models()

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    # 微信接入url (wx.huigo.com)
    url(r'^$', WeChatAccessView.as_view()),
    # 测试获取access_token
    url(r'^token/$', GetAccessTokenView.as_view()),

    url(r'^api/', include('api.urls',namespace='api')),
]
