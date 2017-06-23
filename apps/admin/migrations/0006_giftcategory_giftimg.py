# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_auto_20170617_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(verbose_name='名称', max_length=12)),
                ('url', models.CharField(verbose_name='背景图片', max_length=128)),
                ('upload_time', models.DateField(verbose_name='logo', max_length=128)),
            ],
            options={
                'verbose_name_plural': '基础数据-分类',
                'db_table': 'gift_category',
                'verbose_name': '基础数据-分类',
            },
        ),
        migrations.CreateModel(
            name='GiftImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(verbose_name='名称', max_length=12)),
                ('url', models.CharField(verbose_name='背景图片', max_length=128)),
                ('upload_time', models.DateField(verbose_name='logo', max_length=128)),
            ],
            options={
                'verbose_name_plural': '基础数据-图片',
                'db_table': 'gift_img',
                'verbose_name': '基础数据-图片',
            },
        ),
    ]
