# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170703_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logwx',
            name='errcode',
            field=models.CharField(max_length=16, verbose_name='错误编码'),
        ),
        migrations.AlterField(
            model_name='logwx',
            name='errmsg',
            field=models.CharField(max_length=128, verbose_name='错误信息'),
        ),
        migrations.AlterField(
            model_name='logwx',
            name='type',
            field=models.CharField(max_length=2, verbose_name='错误类型(0:;1:send_temp,2:cron_giftcard_balance_change,3:CardEditView,4:UploadPageView,5:,6:giftcard_pay_done,7:CardDelView,8:modifyCardStock)', default='0'),
        ),
    ]
