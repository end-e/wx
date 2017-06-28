# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0023_auto_20170624_1802'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GiftCategory',
        ),
        migrations.RemoveField(
            model_name='giftthemeitem',
            name='wx_card_id',
        ),
        migrations.AddField(
            model_name='giftthemeitem',
            name='card_id',
            field=models.IntegerField(null=True, verbose_name='微信返回ID', blank=True),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='background_pic',
            field=models.IntegerField(verbose_name='背景图片'),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='logo',
            field=models.IntegerField(verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='giftpage',
            name='banner_pic',
            field=models.IntegerField(verbose_name='banner图片'),
        ),
        migrations.AlterField(
            model_name='gifttheme',
            name='theme_pic',
            field=models.IntegerField(verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='giftthemepicitem',
            name='background_pic',
            field=models.IntegerField(verbose_name='背景图片'),
        ),
    ]
