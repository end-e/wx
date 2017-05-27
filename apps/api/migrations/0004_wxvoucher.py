# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170508_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxVoucher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('voucher_no', models.CharField(verbose_name='编号', max_length=32, default='')),
                ('voucher_name', models.CharField(verbose_name='名称', max_length=32, default='')),
                ('voucher_price', models.DecimalField(verbose_name='面值', decimal_places=2, max_digits=12)),
                ('begin_date', models.DateTimeField(null=True, verbose_name='开始日期', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='截至日期', blank=True)),
                ('voucher_image', models.ImageField(null=True, verbose_name='图片', blank=True, upload_to='')),
            ],
            options={
                'managed': False,
                'db_table': 'wx_voucher',
            },
        ),
    ]
