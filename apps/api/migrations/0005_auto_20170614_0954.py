# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_wxvoucher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='log',
            name='last_purchserial',
        ),
        migrations.AlterField(
            model_name='log',
            name='type',
            field=models.CharField(verbose_name='错误类型 1:token获取;2:信息推送', max_length=2, choices=[('01', 'token获取'), ('02', '消费信息'), ('03', '卡卷核销')]),
        ),
    ]
