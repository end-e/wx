# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0044_auto_20170727_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopgoodimg',
            name='status',
        ),
        migrations.RemoveField(
            model_name='shopgoodproperty',
            name='status',
        ),
    ]
