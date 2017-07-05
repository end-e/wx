# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0029_auto_20170703_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftBalanceChangeLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('last_serial', models.BigIntegerField(verbose_name='每次轮询的最后一个ID')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'gift_card_balance_change_log',
            },
        ),
    ]
