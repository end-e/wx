from django.db import models


class Voucher(models.Model):
    voucher_no = models.CharField(max_length=32, default='', verbose_name=u'券编号')
    voucher_name = models.CharField(max_length=32, default='', verbose_name=u'券名称')
    voucher_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'券面值')
    begin_date = models.DateTimeField(blank=True, null=True, verbose_name=u'开始日期')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'截至日期')
    voucher_image = models.ImageField(blank=True, null=True, verbose_name=u'券图片')

