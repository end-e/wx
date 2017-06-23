# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0011_auto_20170620_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftthemeitem',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='giftthemepicitem',
            name='theme',
        ),
        migrations.AddField(
            model_name='gifttheme',
            name='sku_title_first',
            field=models.CharField(max_length=1, verbose_name='突出商品名(1:是,0:否)', default='0'),
        ),
        migrations.AddField(
            model_name='giftthemeitem',
            name='theme_id',
            field=models.IntegerField(default=1, verbose_name='主题ID'),
        ),
        migrations.AddField(
            model_name='giftthemepicitem',
            name='theme_id',
            field=models.IntegerField(default=1, verbose_name='主题ID'),
        ),
        migrations.AlterField(
            model_name='gifttheme',
            name='category',
            field=models.SmallIntegerField(verbose_name='所属分类', blank=True, null=True),
        ),
    ]
