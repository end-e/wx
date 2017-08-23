# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0057_auto_20170731_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporder',
            name='openid',
        ),
        migrations.AlterField(
            model_name='shoporder',
            name='customer',
            field=models.CharField(default=0, verbose_name='用户ID', max_length=50),
        ),
    ]
