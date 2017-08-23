# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0051_auto_20170728_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopbannerinfo',
            name='banner',
            field=models.IntegerField(default=0, verbose_name='bannerID'),
        ),
    ]
