# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0028_auto_20170703_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftcardcode',
            old_name='card_id',
            new_name='wx_card_id',
        ),
    ]
