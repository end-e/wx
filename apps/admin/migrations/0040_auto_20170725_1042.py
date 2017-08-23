# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0039_auto_20170725_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoptheme',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='开始日期'),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='end_time',
            field=models.DateTimeField(verbose_name='结束日期'),
        ),
    ]
