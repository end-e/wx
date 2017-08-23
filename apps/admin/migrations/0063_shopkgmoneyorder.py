# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0062_shopuser_kg_money'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopKgMoneyOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sn', models.CharField(verbose_name='编号', unique=True, max_length=16)),
                ('kg_money', models.IntegerField(verbose_name='宽广豆数量')),
                ('pay_type', models.CharField(verbose_name='支付类型', max_length=1)),
                ('total_pay', models.DecimalField(verbose_name='支付合计', max_digits=8, decimal_places=2)),
                ('customer', models.CharField(verbose_name='用户openID', max_length=50, default='0')),
                ('status', models.CharField(verbose_name='订单状态', max_length=1, default='0')),
                ('save_time', models.DateTimeField(verbose_name='下单时间', default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'shop_kgmoney_order',
            },
        ),
    ]
