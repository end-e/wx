# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0021_auto_20170623_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='status',
            field=models.CharField(max_length=1, verbose_name='状态(0:线下失效,1:线下生效,2:已上线)', default='1'),
        ),
    ]
