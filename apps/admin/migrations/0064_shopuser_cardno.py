# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0063_shopkgmoneyorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='cardNo',
            field=models.CharField(verbose_name='会员卡号', default='', max_length=10),
        ),
    ]
