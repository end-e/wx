# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0052_shopbannerinfo_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopbannerinfo',
            name='name',
            field=models.CharField(verbose_name='名称', default='', max_length=12),
        ),
    ]
