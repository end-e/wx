# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0058_auto_20170731_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoporder',
            name='status',
            field=models.CharField(max_length=1, default='0', verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='address',
            field=models.CharField(max_length=12, default='', verbose_name='配送地址ID'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='customer',
            field=models.CharField(max_length=50, default='0', verbose_name='用户ID'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='express',
            field=models.IntegerField(verbose_name='快递', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='remark',
            field=models.TextField(verbose_name='备注留言', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='save_time',
            field=models.DateTimeField(verbose_name='下单时间', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='sign_time',
            field=models.DateTimeField(verbose_name='签收时间', null=True, blank=True),
        ),
    ]
