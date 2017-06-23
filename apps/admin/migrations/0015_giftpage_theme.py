# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0014_auto_20170620_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftpage',
            name='themes',
            field=models.CharField(verbose_name='主题列表', default='', max_length=256),
        ),
    ]
