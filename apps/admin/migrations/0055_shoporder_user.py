# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0054_shoptheme_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoporder',
            name='user',
            field=models.IntegerField(default=0, verbose_name='下单用户'),
        ),
    ]
