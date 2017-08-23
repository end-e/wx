# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0056_shopuser_extend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopaddress',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='shoporder',
            name='user',
        ),
        migrations.AddField(
            model_name='shopaddress',
            name='openid',
            field=models.CharField(verbose_name='用户ID', default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='shoporder',
            name='openid',
            field=models.CharField(verbose_name='用户ID', default=0, max_length=50),
        ),
    ]
