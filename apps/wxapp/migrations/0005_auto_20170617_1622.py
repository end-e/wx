# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0004_auto_20170617_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discode',
            name='use_time',
            field=models.DateTimeField(verbose_name='使用时间', null=True),
        ),
    ]
