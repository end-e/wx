# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0018_auto_20170621_0925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftcard',
            old_name='background_pic_url',
            new_name='background_pic',
        ),
        migrations.RenameField(
            model_name='giftcard',
            old_name='logo_url',
            new_name='logo',
        ),
    ]
