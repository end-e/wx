# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0046_auto_20170727_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopBanner',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=16, verbose_name='')),
                ('desc', models.CharField(max_length=32, verbose_name='')),
                ('begin_time', models.DateTimeField(verbose_name='')),
                ('end_time', models.DateTimeField(verbose_name='')),
                ('sort', models.CharField(max_length=1, verbose_name='')),
                ('status', models.CharField(max_length=1, verbose_name='')),
            ],
            options={
                'db_table': 'shop_banner',
            },
        ),
        migrations.CreateModel(
            name='ShopBannerInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('img', models.ImageField(verbose_name='图片', upload_to='shop/%Y/%m')),
                ('type', models.CharField(max_length=1, verbose_name='类型（0:无导向;1:导向商品;2:导向专题）')),
                ('target_id', models.IntegerField(verbose_name='跳转目标', null=True, blank=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('begin_time', models.DateTimeField(verbose_name='开始日期')),
                ('end_time', models.DateTimeField(verbose_name='结束日期')),
                ('sort', models.CharField(max_length=2, default=1, verbose_name='排序')),
            ],
            options={
                'db_table': 'shop_banner_info',
            },
        ),
        migrations.RemoveField(
            model_name='shoptheme',
            name='begin_time',
        ),
        migrations.RemoveField(
            model_name='shoptheme',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='shoptheme',
            name='sort',
        ),
    ]
