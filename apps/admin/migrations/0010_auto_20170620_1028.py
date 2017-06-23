# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0009_gifttheme_giftthemeitem_giftthemepicitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gifttheme',
            old_name='category_index',
            new_name='category',
        ),
    ]
