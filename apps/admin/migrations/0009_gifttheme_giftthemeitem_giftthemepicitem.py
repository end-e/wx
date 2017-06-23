# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0008_auto_20170620_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=12, verbose_name='主题名称')),
                ('theme_pic', models.CharField(max_length=128, verbose_name='封面图片')),
                ('title_color', models.CharField(max_length=7, verbose_name='主题字体颜色', default='#FB966E')),
                ('category_index', models.IntegerField(max_length=5, verbose_name='所属分类')),
                ('create_time', models.DateField(max_length=128, verbose_name='创建日期', default=datetime.datetime.now)),
                ('status', models.CharField(max_length=1, verbose_name='状态', default='0')),
            ],
            options={
                'verbose_name': '基础数据-主题',
                'verbose_name_plural': '基础数据-主题',
                'db_table': 'gift_theme',
            },
        ),
        migrations.CreateModel(
            name='GiftThemeItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('card_id', models.CharField(max_length=32, verbose_name='微信返回ID', blank=True, null=True)),
                ('title', models.CharField(max_length=12, verbose_name='名称')),
                ('theme', models.ForeignKey(to='admin.GiftTheme')),
            ],
            options={
                'verbose_name': '基础数据-主题-item',
                'verbose_name_plural': '基础数据-主题-item',
                'db_table': 'gift_theme_item',
            },
        ),
        migrations.CreateModel(
            name='GiftThemePicItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('background_pic', models.CharField(max_length=128, verbose_name='背景图片')),
                ('msg', models.CharField(max_length=32, verbose_name='默认祝福语')),
                ('theme', models.ForeignKey(to='admin.GiftTheme')),
            ],
            options={
                'verbose_name': '基础数据-分类-picItem',
                'verbose_name_plural': '基础数据-分类-picItem',
                'db_table': 'gift_category_pic_item',
            },
        ),
    ]
