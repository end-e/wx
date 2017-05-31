# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nav',
            name='icon',
            field=models.CharField(null=True, max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='status',
            field=models.CharField(default='0', max_length=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='rolenav',
            name='nav_id',
            field=models.ForeignKey(null=True, to='admin.Nav', blank=True),
        ),
        migrations.AlterField(
            model_name='rolenav',
            name='role_id',
            field=models.ForeignKey(null=True, to='admin.Role', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(unique=True, max_length=45, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(default='', max_length=15, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(default='0', max_length=1, verbose_name='状态'),
        ),
        migrations.AlterUniqueTogether(
            name='rolenav',
            unique_together=set([('role_id', 'nav_id')]),
        ),
    ]
