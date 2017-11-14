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


class CashCoupon(models.Model):
    code_type = models.CharField(max_length=128, verbose_name=u'码型',
                                 choices=(('CODE_TYPE_TEXT', u'文本'),
                                          ('CODE_TYPE_BARCODE', u'一维码'),
                                          ('CODE_TYPE_QRCODE', u'二维码'),
                                          ('CODE_TYPE_ONLY_QRCODE', u'二维码无code显示'),
                                          ('CODE_TYPE_ONLY_BARCODE', u'一维码无code显示'))
                                 )
    brand_name = models.CharField(max_length=36, verbose_name=u'商户名字')
    title = models.CharField(max_length=27, verbose_name=u'卡券名')
    color = models.CharField(max_length=16, verbose_name=u'券颜色')
    notice = models.CharField(max_length=48, verbose_name=u'卡券使用提醒')
    description = models.CharField(max_length=3072, verbose_name=u'卡券使用说明')
    type = models.CharField(max_length=128, verbose_name=u'使用时间类型',default='DATE_TYPE_FIX_TIME_RANGE',
                            choices=(('DATE_TYPE_FIX_TIME_RANGE', u'固定日期'),
                                     ('DATE_TYPE_FIX_TERM', u'领取后计算固定日期'))
                            )
    begin_time = models.DateField(verbose_name=u'起用时间')
    end_time = models.DateField(verbose_name=u'结束时间')
    get_limit = models.IntegerField(verbose_name=u'每人可领券的数量限制',default=1)
    use_limit = models.IntegerField(verbose_name=u'每人可核销的数量限制',default=1)
    least_cost = models.IntegerField(verbose_name=u'代金券起用金额，单位分')
    reduce_cost = models.IntegerField(verbose_name=u'代金券减免金额，单位分')
    card_id = models.CharField(max_length=32, verbose_name=u'微信端卡券ID',blank=True,null=True)
    is_passing = models.CharField(max_length=1, default='0', verbose_name=u'是否通过微信审核')

    class Meta:
        verbose_name = u'微信卡券详情'
        verbose_name_plural = verbose_name
        db_table = 'cash_coupon'
