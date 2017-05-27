# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_auto_20170527_1029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rolenav',
            old_name='nav_id',
            new_name='nav',
        ),
        migrations.RenameField(
            model_name='rolenav',
            old_name='role_id',
            new_name='role',
        ),
        migrations.AlterUniqueTogether(
            name='rolenav',
            unique_together=set([('role', 'nav')]),
        ),
    ]
