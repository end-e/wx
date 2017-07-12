# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0026_giftcardcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcardcode',
            name='code',
            field=models.CharField(verbose_name='线下Code', max_length=12, unique=True),
        ),
    ]
