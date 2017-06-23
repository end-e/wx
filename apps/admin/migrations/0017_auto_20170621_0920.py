# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0016_giftpage_home_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftpage',
            old_name='page_id',
            new_name='wx_page_id',
        ),
        migrations.RenameField(
            model_name='giftpage',
            old_name='home_url',
            new_name='wx_page_url',
        ),
    ]
