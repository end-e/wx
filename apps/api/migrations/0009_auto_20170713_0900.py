# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20170707_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logwx',
            name='remark',
            field=models.CharField(max_length=256, verbose_name='备注', null=True, blank=True),
        ),
    ]
