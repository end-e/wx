# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0059_auto_20170801_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoporder',
            name='price',
            field=models.DateTimeField(max_length=16, verbose_name='价格'),
        ),
    ]
