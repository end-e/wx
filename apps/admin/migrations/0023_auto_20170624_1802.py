# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0022_auto_20170624_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftthemeitem',
            old_name='card_id',
            new_name='wx_card_id',
        ),
    ]
