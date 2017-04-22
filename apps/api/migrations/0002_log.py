# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('errmsg', models.CharField(verbose_name='错误信息', max_length=60)),
                ('errcode', models.CharField(verbose_name='错误编码', max_length=8)),
                ('type', models.CharField(choices=[('01', 'token获取'), ('02', '消费信息'), ('03', '卡卷核销')], verbose_name='错误类型', max_length=2)),
                ('add_time', models.DateTimeField(verbose_name='添加时间', default=datetime.datetime.now)),
            ],
        ),
    ]
