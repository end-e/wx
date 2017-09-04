# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models


class CashCouponsImg(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'资源名称')
    url = models.CharField(max_length=128, verbose_name=u'资源地址')
    create_time = models.DateField(max_length=128, verbose_name='添加时间', default=datetime.now)
    SHOP_CODE_CHOICES = (
        ('C001', '德汇店'),
        ('C002', '商城店'),
        ('C003', '双百店'),
        ('C004', '滦河店'),
        ('C005', '宽城广场店'),
        ('C006', '宽城购物店'),
        ('C008', '围场店'),
        ('C009', '丰润店'),
        ('C010', '丰白店'),
        ('C013', '平泉店'),
        ('C014', '滦平店'),
        ('C015', '隆华店'),
        ('C016', '双滦广场店'),
        ('C017', '安定里店'),
        ('C018', '奥体店'),
        ('C019', '天山店'),
        ('C020', '美神店'),
        ('C023', '丰宁二店'),
        ('C024', '嘉和店'),
        ('C025', '名都店'),
        ('C026', '下板城店'),
        ('T001', '迁安店'),
    )
    shop_code = models.CharField(max_length=5, verbose_name=u'所属门店', choices=SHOP_CODE_CHOICES, default='0')
    status = models.CharField(max_length=1, verbose_name=u'可用状态', default=1)

    class Meta:
        verbose_name = u'微信卡券素材资源'
        verbose_name_plural = verbose_name
        db_table = 'cash_coupons_img'
