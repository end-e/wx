# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0025_auto_20170628_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCardCode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('card_id', models.IntegerField(verbose_name='卡实例ID')),
                ('code', models.CharField(max_length=12, verbose_name='线下Code')),
            ],
            options={
                'db_table': 'gift_card_code',
            },
        ),
    ]
