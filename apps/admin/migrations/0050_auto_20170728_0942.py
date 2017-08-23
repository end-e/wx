# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0049_auto_20170728_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopbanner',
            old_name='create_time',
            new_name='save_time',
        ),
        migrations.RenameField(
            model_name='shopbannerinfo',
            old_name='create_time',
            new_name='save_time',
        ),
        migrations.RenameField(
            model_name='shopgood',
            old_name='create_time',
            new_name='save_time',
        ),
        migrations.RenameField(
            model_name='shoporder',
            old_name='create_time',
            new_name='save_time',
        ),
        migrations.RenameField(
            model_name='shoptheme',
            old_name='create_time',
            new_name='save_time',
        ),
    ]
