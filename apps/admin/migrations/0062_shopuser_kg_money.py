# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0061_auto_20170810_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='kg_money',
            field=models.IntegerField(verbose_name='宽广豆', default=0),
        ),
    ]
