# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0042_auto_20170727_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='banner',
            field=models.ImageField(verbose_name='banner图', upload_to='shop/%Y/%m', blank=True, null=True),
        ),
    ]
