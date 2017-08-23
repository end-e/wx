# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0038_auto_20170724_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='sort',
            field=models.CharField(verbose_name='排序', default=1, max_length=2),
        ),
        migrations.AlterField(
            model_name='shopgood',
            name='img',
            field=models.ImageField(verbose_name='封面图', upload_to='shop/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='create_time',
            field=models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='desc',
            field=models.CharField(verbose_name='描述', null=True, blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='img',
            field=models.ImageField(verbose_name='图片', upload_to='shop/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='shoptheme',
            name='sort',
            field=models.CharField(verbose_name='排序', default=1, max_length=2),
        ),
    ]
