# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import MembersBoundView, MembersImageView

urlpatterns = [
    # 会员绑定页面
    url(r'^membersbound', MembersBoundView.as_view(), name="members_bound"),
    # 会员二维码
    url(r'^membersimage', MembersImageView.as_view(), name="members_image")
]