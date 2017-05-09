# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WechatMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nikename', models.CharField(max_length=1000, verbose_name='昵称', null=True)),
                ('sex', models.CharField(choices=[('1', '男'), ('2', '女'), ('0', '未知')], max_length=1, null=True)),
                ('city', models.CharField(max_length=45, verbose_name='城市', null=True)),
                ('country', models.CharField(max_length=45, verbose_name='省份', null=True)),
                ('province', models.CharField(max_length=45, verbose_name='国家', null=True)),
                ('openid', models.CharField(max_length=100, verbose_name='openid')),
                ('telphone', models.CharField(max_length=20, verbose_name='手机号')),
                ('attentiontime', models.DateTimeField(default=datetime.datetime.now, verbose_name='绑定时间')),
                ('username', models.CharField(max_length=45, verbose_name='会员姓名')),
                ('membernumber', models.CharField(max_length=45, verbose_name='会员卡号')),
            ],
            options={
                'verbose_name_plural': '微信会员绑定',
                'verbose_name': '微信会员绑定',
            },
        ),
        migrations.DeleteModel(
            name='AccessToken',
        ),
    ]
