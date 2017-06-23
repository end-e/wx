# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0004_auto_20170527_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=12, verbose_name='名称')),
                ('card_id', models.CharField(blank=True, null=True, max_length=32, verbose_name='微信返回ID')),
                ('background_pic_url', models.CharField(max_length=128, verbose_name='背景图片')),
                ('logo_url', models.CharField(max_length=128, verbose_name='logo')),
                ('init_balance', models.DecimalField(max_digits=10, verbose_name='初始金额', decimal_places=2)),
                ('price', models.DecimalField(max_digits=10, verbose_name='售价', decimal_places=2)),
                ('brand_name', models.CharField(max_length=128, verbose_name='商户名称')),
                ('quantity', models.IntegerField(verbose_name='库存数量')),
            ],
            options={
                'verbose_name': '礼品卡信息',
                'verbose_name_plural': '礼品卡信息',
                'db_table': 'gift_card',
            },
        ),
        migrations.AlterField(
            model_name='rolenav',
            name='nav',
            field=models.ForeignKey(blank=True, related_name='navs', to='admin.Nav', null=True),
        ),
    ]
