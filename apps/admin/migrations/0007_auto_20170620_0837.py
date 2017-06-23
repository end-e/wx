# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_giftcategory_giftimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcard',
            name='status',
            field=models.CharField(max_length=1, default='0', verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='giftcategory',
            name='status',
            field=models.CharField(max_length=1, default='0', verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='giftimg',
            name='status',
            field=models.CharField(max_length=1, default='0', verbose_name='状态'),
        ),
    ]
