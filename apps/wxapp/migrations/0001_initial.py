# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('voucher_no', models.CharField(verbose_name='券编号', max_length=32, default='')),
                ('voucher_name', models.CharField(verbose_name='券名称', max_length=32, default='')),
                ('voucher_price', models.DecimalField(verbose_name='券面值', decimal_places=2, max_digits=12)),
                ('begin_date', models.DateTimeField(null=True, verbose_name='开始日期', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='截至日期', blank=True)),
                ('voucher_image', models.ImageField(null=True, verbose_name='券图片', upload_to='', blank=True)),
            ],
        ),
    ]
