# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0032_auto_20170705_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftorder',
            name='order_id',
            field=models.CharField(verbose_name='订单号', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='giftorderinfo',
            name='code',
            field=models.CharField(verbose_name='code', max_length=32, unique=True),
        ),
    ]
