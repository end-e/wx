# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0065_auto_20170822_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporder',
            name='address',
        ),
        migrations.AddField(
            model_name='shoporder',
            name='snap_address',
            field=models.CharField(verbose_name='配送地址ID', default='', max_length=100),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='snap_img',
            field=models.CharField(verbose_name='订单快照图片', default='', max_length=64),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='snap_name',
            field=models.CharField(verbose_name='订单快照名称', default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='shopgood',
            name='img',
            field=models.ImageField(verbose_name='封面图', upload_to='shop/%Y/%m', max_length=64),
        ),
    ]
