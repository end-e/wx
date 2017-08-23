# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0066_auto_20170823_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoporder',
            name='name',
            field=models.CharField(default='', verbose_name='收件人', max_length=12),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='tel',
            field=models.CharField(default='', verbose_name='联系电话', max_length=12),
        ),
    ]
