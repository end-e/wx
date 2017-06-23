# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0015_giftpage_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftpage',
            name='home_url',
            field=models.CharField(verbose_name='货架首页地址', null=True, max_length=128, blank=True),
        ),
    ]
