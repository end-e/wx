# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0020_auto_20170621_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gifttheme',
            name='category',
        ),
        migrations.AlterField(
            model_name='giftpage',
            name='themes',
            field=models.CharField(verbose_name='主题列表', default='', max_length=128),
        ),
    ]
