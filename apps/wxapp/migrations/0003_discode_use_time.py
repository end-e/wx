# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0002_auto_20170614_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='discode',
            name='use_time',
            field=models.DateTimeField(verbose_name='使用时间', default=datetime.datetime.now),
        ),
    ]
