# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


# Create your models here.
class AccessToken(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    access_token = models.CharField(max_length=512, verbose_name=u'全局票据')
    expires_in = models.CharField(max_length=4, verbose_name=u'生命周期')

    class Meta:
        verbose_name = u'access_token'
        verbose_name_plural = verbose_name


class LogWx(models.Model):
    errmsg = models.CharField(max_length=128, verbose_name=u'错误信息')
    errcode = models.CharField(max_length=16, verbose_name=u'错误编码')
    type = models.CharField(max_length=2,default='0',
                            verbose_name='错误类型(0:cron_gift_compare_order;1:send_temp,2:cron_gift_change_balance,'
                                         '3:CardEditView,4:UploadPageView,5:upCode,6:giftcard_pay_done,7:CardDelView,'
                                         '8:modifyCardStock)'
                            )
    remark = models.CharField(max_length=256, verbose_name='备注', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    repeat_status = models.CharField(blank=True,null=True,max_length=1,verbose_name=u'重发状态')

    class Meta:
        db_table='log_wx'


class LogShop(models.Model):
    errmsg = models.CharField(max_length=128, verbose_name=u'错误信息')
    errcode = models.CharField(max_length=16, verbose_name=u'错误编码')
    remark = models.CharField(max_length=256, verbose_name='备注', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table='log_shop'


