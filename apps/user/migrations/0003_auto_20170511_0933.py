# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20170509_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatmembers',
            name='openid',
            field=models.CharField(verbose_name='openid', unique=True, max_length=100),
        ),
    ]
