# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0037_auto_20170724_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopgood',
            old_name='is_host',
            new_name='is_hot',
        ),
        migrations.AddField(
            model_name='shopgood',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创建日期'),
        ),
        migrations.AddField(
            model_name='shopgood',
            name='stock',
            field=models.SmallIntegerField(default=0, verbose_name='库存'),
        ),
    ]
