# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='access_token',
            field=models.CharField(max_length=512, null=True, blank=True, verbose_name='token'),
        ),
        migrations.AddField(
            model_name='log',
            name='last_purchserial',
            field=models.CharField(max_length=8, null=True, blank=True, verbose_name='上一次最后一个单号'),
        ),
        migrations.AddField(
            model_name='log',
            name='open_id',
            field=models.CharField(max_length=100, null=True, blank=True, verbose_name=''),
        ),
    ]
