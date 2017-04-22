# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('add_time', models.DateTimeField(verbose_name='添加时间', default=datetime.datetime.now)),
                ('access_token', models.CharField(verbose_name='全局票据', max_length=512)),
                ('expires_in', models.CharField(verbose_name='生命周期', max_length=4)),
            ],
            options={
                'verbose_name': 'access_token',
                'verbose_name_plural': 'access_token',
            },
        ),
    ]
