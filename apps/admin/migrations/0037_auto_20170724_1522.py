# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0036_auto_20170712_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=12, verbose_name='收件人')),
                ('tel', models.CharField(max_length=12, verbose_name='联系电话')),
                ('province', models.CharField(max_length=12, verbose_name='省')),
                ('city', models.CharField(max_length=12, verbose_name='市')),
                ('county', models.CharField(max_length=12, verbose_name='县区')),
                ('is_default', models.CharField(max_length=1, verbose_name='默认地址')),
            ],
            options={
                'db_table': 'shop_address',
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('parent', models.IntegerField(verbose_name='父级分类')),
                ('status', models.CharField(max_length=1, verbose_name='状态')),
            ],
            options={
                'db_table': 'shop_category',
            },
        ),
        migrations.CreateModel(
            name='ShopExpress',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('tel', models.CharField(max_length=11, verbose_name='电话')),
                ('price', models.DecimalField(max_digits=8, verbose_name='价格', decimal_places=2)),
                ('status', models.CharField(max_length=1, verbose_name='状态')),
            ],
            options={
                'db_table': 'shop_express',
            },
        ),
        migrations.CreateModel(
            name='ShopGood',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('sn', models.CharField(max_length=32, verbose_name='编码')),
                ('price', models.DecimalField(max_digits=8, verbose_name='价格', decimal_places=2)),
                ('img', models.ImageField(verbose_name='预览图', upload_to='upload')),
                ('category', models.IntegerField(verbose_name='所属分类')),
                ('is_host', models.CharField(max_length=1, verbose_name='热卖')),
                ('is_new', models.CharField(max_length=1, verbose_name='新品')),
                ('status', models.CharField(max_length=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 'shop_good',
            },
        ),
        migrations.CreateModel(
            name='ShopOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('sn', models.CharField(max_length=16, verbose_name='编号')),
                ('price', models.CharField(max_length=16, verbose_name='价格')),
                ('express', models.IntegerField(verbose_name='快递')),
                ('create_time', models.DateTimeField(verbose_name='下单时间')),
                ('sign_time', models.DateTimeField(verbose_name='签收时间')),
                ('remark', models.TextField(verbose_name='备注留言')),
                ('customer', models.CharField(max_length=12, verbose_name='用户ID')),
                ('address', models.CharField(max_length=12, verbose_name='配送地址ID')),
            ],
            options={
                'db_table': 'shop_order',
            },
        ),
        migrations.CreateModel(
            name='ShopOrderInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order_sn', models.CharField(max_length=16, verbose_name='订单编号')),
                ('good_sn', models.CharField(max_length=32, verbose_name='商品ID')),
                ('good_num', models.IntegerField(verbose_name='商品数量')),
            ],
            options={
                'db_table': 'shop_order_info',
            },
        ),
        migrations.CreateModel(
            name='ShopTheme',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=12, verbose_name='名称')),
                ('desc', models.CharField(max_length=32, verbose_name='描述')),
                ('img', models.ImageField(verbose_name='图片', upload_to='upload')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('end_time', models.DateTimeField(verbose_name='到期时间')),
                ('sort', models.CharField(max_length=2, verbose_name='排序')),
            ],
            options={
                'db_table': 'shop_theme',
            },
        ),
        migrations.CreateModel(
            name='ShopThemeInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('theme_id', models.IntegerField()),
                ('good_sn', models.IntegerField()),
            ],
            options={
                'db_table': 'shop_theme_info',
            },
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='status',
            field=models.CharField(max_length=1, verbose_name='状态(0:封存;1:禁用,2:启用,9:上线;)', default='2'),
        ),
    ]
