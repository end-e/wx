# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0005_auto_20170617_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discode',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='discode',
            name='has_usable',
        ),
        migrations.RemoveField(
            model_name='discode',
            name='use_time',
        ),
        migrations.AddField(
            model_name='discode',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='到期时间'),
        ),
        migrations.AddField(
            model_name='discode',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='开始时间'),
        ),
    ]
