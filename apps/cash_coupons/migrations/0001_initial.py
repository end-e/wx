# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashCoupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('code_type', models.CharField(verbose_name='码型', choices=[('CODE_TYPE_TEXT', '文本'), ('CODE_TYPE_BARCODE', '一维码'), ('CODE_TYPE_QRCODE', '二维码'), ('CODE_TYPE_ONLY_QRCODE', '二维码无code显示'), ('CODE_TYPE_ONLY_BARCODE', '一维码无code显示')], max_length=128)),
                ('brand_name', models.CharField(verbose_name='商户名字', max_length=36)),
                ('title', models.CharField(verbose_name='卡券名', max_length=27)),
                ('color', models.CharField(verbose_name='券颜色', max_length=16)),
                ('notice', models.CharField(verbose_name='卡券使用提醒', max_length=48)),
                ('description', models.CharField(verbose_name='卡券使用说明', max_length=3072)),
                ('type', models.CharField(verbose_name='使用时间类型', choices=[('DATE_TYPE_FIX_TIME_RANGE', '固定日期'), ('DATE_TYPE_FIX_TERM', '领取后计算固定日期')], default='DATE_TYPE_FIX_TIME_RANGE', max_length=128)),
                ('begin_time', models.DateField(verbose_name='起用时间')),
                ('end_time', models.DateField(verbose_name='结束时间')),
                ('get_limit', models.IntegerField(verbose_name='每人可领券的数量限制', default=1)),
                ('use_limit', models.IntegerField(verbose_name='每人可核销的数量限制', default=1)),
                ('least_cost', models.IntegerField(verbose_name='代金券起用金额，单位分')),
                ('reduce_cost', models.IntegerField(verbose_name='代金券减免金额，单位分')),
                ('card_id', models.CharField(verbose_name='微信端卡券ID', blank=True, null=True, max_length=32)),
                ('is_passing', models.CharField(verbose_name='是否通过微信审核', default='0', max_length=1)),
            ],
            options={
                'verbose_name': '微信卡券详情',
                'verbose_name_plural': '微信卡券详情',
                'db_table': 'cash_coupon',
            },
        ),
        migrations.CreateModel(
            name='CashCouponsImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name='资源名称', max_length=50)),
                ('url', models.CharField(verbose_name='资源地址', max_length=128)),
                ('create_time', models.DateField(verbose_name='添加时间', default=datetime.datetime.now, max_length=128)),
                ('status', models.CharField(verbose_name='可用状态', default=1, max_length=1)),
            ],
            options={
                'verbose_name': '微信卡券素材资源',
                'verbose_name_plural': '微信卡券素材资源',
                'db_table': 'cash_coupons_img',
            },
        ),
    ]
