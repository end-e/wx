# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0003_discode_use_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discode',
            name='use_time',
            field=models.DateTimeField(verbose_name='使用时间'),
        ),
    ]
