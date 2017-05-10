# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import MembersBoundView

urlpatterns = [
    # 会员绑定页面
    url(r'^membersbound', MembersBoundView.as_view(), name="members_bound")
]