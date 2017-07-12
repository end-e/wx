# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20170703_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='logwx',
            name='type',
            field=models.CharField(verbose_name='错误类型(0:程序错误;1:微信模板消息,2:礼品卡余额)', max_length=2, default='0'),
        ),
        migrations.AlterField(
            model_name='logwx',
            name='remark',
            field=models.CharField(null=True, verbose_name='备注', max_length=128, blank=True),
        ),
    ]
