# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0007_auto_20170620_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftcategory',
            name='upload_time',
        ),
        migrations.RemoveField(
            model_name='giftcategory',
            name='url',
        ),
        migrations.RemoveField(
            model_name='giftimg',
            name='upload_time',
        ),
        migrations.AddField(
            model_name='giftcategory',
            name='create_time',
            field=models.DateField(verbose_name='创建日期', default=datetime.datetime.now, max_length=128),
        ),
        migrations.AddField(
            model_name='giftimg',
            name='create_time',
            field=models.DateField(verbose_name='创建日期', default=datetime.datetime.now, max_length=128),
        ),
    ]
