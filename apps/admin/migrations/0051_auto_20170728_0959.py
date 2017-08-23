# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0050_auto_20170728_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoptheme',
            name='begin_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='开始日期'),
        ),
        migrations.AddField(
            model_name='shoptheme',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='结束日期'),
        ),
        migrations.AddField(
            model_name='shoptheme',
            name='sort',
            field=models.CharField(default=1, verbose_name='排序', max_length=2),
        ),
        migrations.AlterField(
            model_name='shopbanner',
            name='save_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='shopbannerinfo',
            name='save_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='save_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间'),
        ),
    ]
