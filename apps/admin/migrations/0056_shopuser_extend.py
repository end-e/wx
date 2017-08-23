# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0055_shoporder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='extend',
            field=models.CharField(verbose_name='', max_length=128, default=''),
        ),
    ]
