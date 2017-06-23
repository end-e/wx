# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0019_auto_20170621_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcard',
            name='description',
            field=models.CharField(max_length=1000, verbose_name='使用说明', default=''),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='max_give',
            field=models.SmallIntegerField(verbose_name='最大赠送次数', default=9999),
        ),
        migrations.AddField(
            model_name='giftcard',
            name='notice',
            field=models.CharField(max_length=12, verbose_name='使用提醒', default=''),
        ),
    ]
