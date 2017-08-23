# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0035_gifttheme_is_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcard',
            name='name',
            field=models.CharField(verbose_name='名称-本地', max_length=12, default='礼品卡'),
        ),
        migrations.AddField(
            model_name='gifttheme',
            name='name',
            field=models.CharField(verbose_name='名称-本地', max_length=12, default='礼品卡'),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='title',
            field=models.CharField(verbose_name='名称-微信', max_length=12),
        ),
        migrations.AlterField(
            model_name='gifttheme',
            name='title',
            field=models.CharField(verbose_name='名称-微信', max_length=12),
        ),
    ]
