# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models


class CashCouponsImg(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'资源名称')
    url = models.CharField(max_length=128, verbose_name=u'资源地址')
    create_time = models.DateField(max_length=128, verbose_name='添加时间', default=datetime.now)
    status = models.CharField(max_length=1, verbose_name=u'可用状态', default=1)

    class Meta:
        verbose_name = u'微信卡券素材资源'
        verbose_name_plural = verbose_name
        db_table = 'cash_coupons_img'
