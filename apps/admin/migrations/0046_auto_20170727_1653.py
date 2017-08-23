# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0045_auto_20170727_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('openid', models.CharField(max_length=50, verbose_name='', unique=True)),
                ('nickname', models.CharField(max_length=10, verbose_name='昵称')),
                ('create_time', models.DateTimeField(verbose_name='创建日期', default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'shop_user',
            },
        ),
        migrations.RenameField(
            model_name='shopaddress',
            old_name='county',
            new_name='country',
        ),
        migrations.AddField(
            model_name='shopaddress',
            name='create_time',
            field=models.DateTimeField(verbose_name='', default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='shopaddress',
            name='detail',
            field=models.CharField(max_length=50, verbose_name='详细地址', default=''),
        ),
        migrations.AddField(
            model_name='shopaddress',
            name='user_id',
            field=models.IntegerField(verbose_name='用户ID', default=0),
        ),
        migrations.AlterField(
            model_name='shopaddress',
            name='is_default',
            field=models.CharField(max_length=1, verbose_name='默认地址', default='0'),
        ),
        migrations.AlterField(
            model_name='shopgood',
            name='sn',
            field=models.CharField(max_length=32, verbose_name='商品编码', unique=True),
        ),
        migrations.AlterField(
            model_name='shopgoodimg',
            name='img',
            field=models.ImageField(upload_to='shop/%Y/%m', verbose_name='商品编码'),
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='sn',
            field=models.CharField(max_length=16, verbose_name='编号', unique=True),
        ),
    ]
