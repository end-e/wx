# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models


class WxVoucher(models.Model):
    voucher_no = models.CharField(max_length=25, verbose_name=u'券编号')
    voucher_name = models.CharField(max_length=50, verbose_name=u'券名称', null=True)
    voucher_price = models.DecimalField(max_length=10, verbose_name=u'券面值')
    start_date = models.DateTimeField(default=datetime.now, verbose_name=u'开始日期')
    end_date = models.DateTimeField(default=datetime.now, verbose_name=u'截至日期')
    voucher_image = models.ImageField(verbose_name=u'券图片')

    class Meta:
        verbose_name = u'微信券'
        verbose_name_plural = verbose_name
        db_table = 'wx_voucher'