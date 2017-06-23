# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0010_auto_20170620_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifttheme',
            name='category',
            field=models.SmallIntegerField(verbose_name='所属分类'),
        ),
    ]
