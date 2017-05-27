# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=32, verbose_name='密码')),
                ('nick', models.CharField(blank=True, null=True, verbose_name='昵称', max_length=15)),
                ('depart', models.CharField(blank=True, null=True, verbose_name='所属部门', max_length=45)),
                ('role', models.CharField(max_length=11, verbose_name='角色')),
                ('status', models.CharField(max_length=1, verbose_name='状态')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='登陆时间')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '用户信息',
                'verbose_name': '用户信息',
            },
        ),
    ]
