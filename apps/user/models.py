# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models


class WechatMembers(models.Model):
    nikename = models.CharField(max_length=1000, verbose_name=u'昵称', null=True)
    sex = models.CharField(max_length=1, choices=(('1', u'男'), ('2', u'女'), ('0', u'未知')), null=True)
    city = models.CharField(max_length=45, verbose_name=u'城市', null=True)
    country = models.CharField(max_length=45, verbose_name=u'省份', null=True)
    province = models.CharField(max_length=45, verbose_name=u'国家', null=True)
    openid = models.CharField(max_length=100, verbose_name=u'openid', unique=True)
    telphone = models.CharField(max_length=20, verbose_name=u'手机号')
    attentiontime = models.DateTimeField(default=datetime.now, verbose_name=u'绑定时间')
    username = models.CharField(max_length=45, verbose_name=u'会员姓名')
    membernumber = models.CharField(max_length=45, verbose_name=u'会员卡号')

    class Meta:
        verbose_name = u'微信会员绑定'
        verbose_name_plural = verbose_name
