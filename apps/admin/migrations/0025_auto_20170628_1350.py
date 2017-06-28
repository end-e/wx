# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0024_auto_20170628_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftthemeitem',
            name='card_id',
        ),
        migrations.AddField(
            model_name='giftthemeitem',
            name='wx_card_id',
            field=models.CharField(max_length=32, verbose_name='微信返回ID', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='background_pic',
            field=models.CharField(max_length=128, verbose_name='背景图片'),
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='logo',
            field=models.CharField(max_length=128, verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='giftpage',
            name='banner_pic',
            field=models.CharField(max_length=128, verbose_name='banner图片'),
        ),
        migrations.AlterField(
            model_name='gifttheme',
            name='theme_pic',
            field=models.CharField(max_length=128, verbose_name='封面图片'),
        ),
        migrations.AlterField(
            model_name='giftthemepicitem',
            name='background_pic',
            field=models.CharField(max_length=128, verbose_name='背景图片'),
        ),
    ]
