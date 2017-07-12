# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0027_auto_20170630_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcardcode',
            name='card_id',
            field=models.CharField(verbose_name='卡实例ID', max_length=32),
        ),
    ]
