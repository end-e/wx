# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0064_shopuser_cardno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopkgmoneyorder',
            old_name='kg_money',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='shopkgmoneyorder',
            old_name='total_pay',
            new_name='price',
        ),
    ]
