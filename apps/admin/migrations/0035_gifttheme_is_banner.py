# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0034_remove_giftorder_accepter_openid'),
    ]

    operations = [
        migrations.AddField(
            model_name='gifttheme',
            name='is_banner',
            field=models.CharField(default='0', verbose_name='状态', max_length=1),
        ),
    ]
