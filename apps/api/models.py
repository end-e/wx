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


class Log(models.Model):
    errmsg = models.CharField(max_length=60, verbose_name=u'错误信息')
    errcode = models.CharField(max_length=8, verbose_name=u'错误编码')
    type = models.CharField(choices=(('01', u'token获取'), ('02', u'消费信息'), ('03', u'卡卷核销')), max_length=2,
                            verbose_name=u'错误类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
