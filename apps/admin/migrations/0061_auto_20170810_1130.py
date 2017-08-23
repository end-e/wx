# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0060_auto_20170801_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoporder',
            name='price',
            field=models.DecimalField(max_digits=8, verbose_name='价格', decimal_places=2),
        ),
    ]
