# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('parent', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=120)),
                ('icon', models.CharField(null=True, max_length=16, blank=True)),
                ('sort', models.IntegerField()),
                ('status', models.CharField(max_length=1)),
            ],
            options={
                'verbose_name_plural': '菜单列表',
                'verbose_name': '菜单列表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('status', models.CharField(max_length=1, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '用户角色',
                'verbose_name': '用户角色',
            },
        ),
        migrations.CreateModel(
            name='RoleNav',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('role_id', models.IntegerField(blank=True, null=True)),
                ('nav_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'RoleNav',
                'verbose_name': 'RoleNav',
            },
        ),
    ]
