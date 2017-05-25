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
    access_token = models.CharField(max_length=512, verbose_name='token', blank=True, null=True)
    open_id = models.CharField(max_length=100, verbose_name='', blank=True, null=True)
    errmsg = models.CharField(max_length=60, verbose_name=u'错误信息')
    errcode = models.CharField(max_length=8, verbose_name=u'错误编码')
    type = models.CharField(choices=(('01', u'token获取'), ('02', u'消费信息'), ('03', u'卡卷核销')), max_length=2,
                            verbose_name=u'错误类型')
    last_purchserial = models.CharField(max_length=8, verbose_name='上一次最后一个单号', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


class WxVoucher(models.Model):
    voucher_no = models.CharField(max_length=32, default='', verbose_name=u'编号')
    voucher_name = models.CharField(max_length=32, default='', verbose_name=u'名称')
    voucher_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'面值')
    begin_date = models.DateTimeField(blank=True, null=True, verbose_name=u'开始日期')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'截至日期')
    voucher_image = models.ImageField(blank=True, null=True, verbose_name=u'图片')

    class Meta:
        managed = False
        db_table = u'wx_voucher'
