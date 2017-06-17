# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisCode',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('dis_code', models.CharField(max_length=6, verbose_name='验证码')),
                ('batch', models.CharField(max_length=2, verbose_name='批次')),
                ('remark', models.CharField(null=True, blank=True, verbose_name='备注', max_length=200)),
                ('has_usable', models.BooleanField(default=False, verbose_name='是否可用')),
            ],
            options={
                'verbose_name_plural': '券验证码',
                'verbose_name': '券验证码',
            },
        ),
        migrations.CreateModel(
            name='PosterImage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('poster_name', models.CharField(max_length=32, default='', verbose_name='海报名称')),
                ('begin_date', models.DateTimeField(null=True, blank=True, verbose_name='开始日期')),
                ('end_date', models.DateTimeField(null=True, blank=True, verbose_name='截至日期')),
                ('poster_image', models.ImageField(null=True, blank=True, verbose_name='海报图片', upload_to='upload')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('product_code', models.CharField(max_length=32, default='', verbose_name='商品编号')),
                ('product_name', models.CharField(max_length=32, default='', verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='单价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('type_flag', models.CharField(max_length=2, default='0', verbose_name='类型 0普通换购商品 1心愿商品')),
                ('enable_flag', models.CharField(max_length=2, default='0', verbose_name='可用标记 0可用 1禁用')),
                ('begin_date', models.DateTimeField(null=True, blank=True, verbose_name='开始日期')),
                ('end_date', models.DateTimeField(null=True, blank=True, verbose_name='截至日期')),
                ('product_weight', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='商品重量 单位千克')),
                ('product_image', models.ImageField(null=True, blank=True, verbose_name='商品图', upload_to='upload/product')),
            ],
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('shop_code', models.CharField(max_length=16, default='', verbose_name='编号')),
                ('shop_name', models.CharField(max_length=32, default='', verbose_name='名称')),
                ('telphone', models.CharField(max_length=20, default='', verbose_name='电话')),
            ],
        ),
        migrations.CreateModel(
            name='VoucherClass',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('class_name', models.CharField(max_length=32, default='', verbose_name='名称')),
            ],
        ),
        migrations.AddField(
            model_name='voucher',
            name='code_flag',
            field=models.CharField(max_length=2, default='0', verbose_name='门店范围 0全部 1市区 2县区 3自由'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='goods_code',
            field=models.CharField(max_length=32, default='', verbose_name='商品码'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='shop_codes',
            field=models.CharField(null=True, blank=True, verbose_name='适用门店', max_length=500),
        ),
        migrations.AddField(
            model_name='voucher',
            name='type_flag',
            field=models.CharField(max_length=2, default='0', verbose_name='类型 0通用 1微信专享'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, verbose_name='原价', max_digits=12),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='voucher_image',
            field=models.ImageField(null=True, blank=True, verbose_name='券图片', upload_to='upload'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='voucher_name',
            field=models.CharField(max_length=32, default='', verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='voucher_no',
            field=models.CharField(max_length=32, default='', verbose_name='优惠码'),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='voucher_price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='优惠价'),
        ),
    ]
