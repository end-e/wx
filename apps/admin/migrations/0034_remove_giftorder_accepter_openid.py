# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0033_auto_20170706_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftorder',
            name='accepter_openid',
        ),
    ]
