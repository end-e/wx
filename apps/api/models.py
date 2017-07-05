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
    errmsg = models.CharField(max_length=60, verbose_name=u'错误信息')
    errcode = models.CharField(max_length=8, verbose_name=u'错误编码')
    type = models.CharField(max_length=2,default='0',
                            verbose_name='错误类型(0:程序错误;1:微信模板消息,2:礼品卡余额,3:礼品卡实例,4:礼品卡货架,5:上传code)')
    remark = models.CharField(max_length=128, verbose_name='备注', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        db_table='log_wx'

