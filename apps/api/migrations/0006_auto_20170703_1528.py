# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170614_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogWx',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('remark', models.CharField(blank=True, verbose_name='', max_length=100, null=True)),
                ('errmsg', models.CharField(verbose_name='错误信息', max_length=60)),
                ('errcode', models.CharField(verbose_name='错误编码', max_length=8)),
                ('add_time', models.DateTimeField(verbose_name='添加时间', default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'log_wx',
            },
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
