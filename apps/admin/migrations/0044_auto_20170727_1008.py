# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0043_shopcategory_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopGoodImg',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('good_sn', models.CharField(max_length=32, verbose_name='商品编码')),
                ('img', models.ImageField(max_length=32, upload_to='', verbose_name='商品编码')),
                ('sort', models.CharField(max_length=2, verbose_name='排序')),
                ('status', models.CharField(max_length=1, default='0', verbose_name='状态')),
            ],
            options={
                'db_table': 'shop_good_img',
            },
        ),
        migrations.CreateModel(
            name='ShopGoodProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('good_sn', models.CharField(max_length=32, verbose_name='商品编码')),
                ('name', models.CharField(max_length=30, verbose_name='属性名')),
                ('detail', models.CharField(max_length=255, verbose_name='属性值')),
                ('sort', models.CharField(max_length=2, verbose_name='排序')),
                ('status', models.CharField(max_length=1, default='0', verbose_name='状态')),
            ],
            options={
                'db_table': 'shop_good_property',
            },
        ),
        migrations.AlterField(
            model_name='shopgood',
            name='sn',
            field=models.CharField(max_length=32, verbose_name='商品编码'),
        ),
        migrations.AlterField(
            model_name='shoporderinfo',
            name='good_sn',
            field=models.CharField(max_length=8, verbose_name='商品编码'),
        ),
        migrations.AlterField(
            model_name='shopthemeinfo',
            name='good_sn',
            field=models.CharField(max_length=8, verbose_name='商品编码'),
        ),
    ]
