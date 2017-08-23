# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0053_shopbannerinfo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoptheme',
            name='banner',
            field=models.ImageField(upload_to='shop/%Y/%m', default='', verbose_name='图片'),
        ),
    ]
