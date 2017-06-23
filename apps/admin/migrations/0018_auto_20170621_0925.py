# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0017_auto_20170621_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftcard',
            old_name='card_id',
            new_name='wx_card_id',
        ),
    ]
