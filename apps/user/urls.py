# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import MembersBoundView, MembersImageView,SuccessView, MembersUnionid

urlpatterns = [
    # 会员绑定页面
    url(r'^membersbound', MembersBoundView.as_view(), name="members_bound"),
    url(r'^success', SuccessView.as_view(), name="success"),
    # 会员二维码
    url(r'^membersimage', MembersImageView.as_view(), name="members_image"),
    # 批量获取已绑定微信会员的unicode
    url(r'^membersunionid', MembersUnionid.as_view(), name="members_unionid")
]
