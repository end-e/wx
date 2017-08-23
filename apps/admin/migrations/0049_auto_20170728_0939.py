# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0048_auto_20170728_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopbanner',
            name='desc',
            field=models.CharField(max_length=32, blank=True, verbose_name='', null=True),
        ),
    ]
