# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0047_auto_20170728_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopbanner',
            name='begin_time',
        ),
        migrations.RemoveField(
            model_name='shopbanner',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='shopbanner',
            name='sort',
        ),
        migrations.AddField(
            model_name='shopbanner',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
    ]
