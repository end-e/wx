# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0040_auto_20170725_1042'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shopthemeinfo',
            unique_together=set([('theme_id', 'good_sn')]),
        ),
    ]
