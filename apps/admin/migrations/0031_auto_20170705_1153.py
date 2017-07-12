# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0030_giftbalancechangelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32, verbose_name='订单号')),
                ('page_id', models.CharField(max_length=64, verbose_name='货架号')),
                ('trans_id', models.CharField(max_length=32, verbose_name='微信支付交易订单号')),
                ('create_time', models.IntegerField(verbose_name='订单创建时间')),
                ('pay_finish_time', models.IntegerField(verbose_name='订单支付时间')),
                ('total_price', models.IntegerField(verbose_name='全部金额')),
                ('open_id', models.CharField(max_length=32, verbose_name='购买者')),
                ('accepter_openid', models.CharField(max_length=32, verbose_name='接收者')),
            ],
            options={
                'db_table': 'gift_order',
            },
        ),
        migrations.CreateModel(
            name='GiftOrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order_id', models.IntegerField(verbose_name='对应gift_order的自增长id')),
                ('card_id', models.CharField(max_length=32, verbose_name='卡类型ID')),
                ('price', models.IntegerField(verbose_name='卡面值')),
                ('code', models.CharField(max_length=32, verbose_name='code')),
            ],
            options={
                'db_table': 'gift_order_info',
            },
        ),
        migrations.AddField(
            model_name='giftbalancechangelog',
            name='status',
            field=models.CharField(default='0', max_length=1, verbose_name='code状态u(0:未销售;1:已销售)'),
        ),
    ]
