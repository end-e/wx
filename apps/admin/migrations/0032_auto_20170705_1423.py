# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0031_auto_20170705_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftbalancechangelog',
            name='status',
        ),
        migrations.RemoveField(
            model_name='giftorder',
            name='page_id',
        ),
        migrations.AddField(
            model_name='giftcardcode',
            name='status',
            field=models.CharField(max_length=1, verbose_name='code状态u(0:未销售;1:已销售)', default='0'),
        ),
    ]
