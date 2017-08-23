# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0041_auto_20170726_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nav',
            name='url',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
