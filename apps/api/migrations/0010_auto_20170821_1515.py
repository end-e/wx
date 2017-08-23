# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20170713_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='logwx',
            name='repeat_status',
            field=models.CharField(null=True, verbose_name='重发状态', max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='logwx',
            name='type',
            field=models.CharField(default='0', verbose_name='错误类型(0:cron_gift_compare_order;1:send_temp,2:cron_gift_change_balance,3:CardEditView,4:UploadPageView,5:upCode,6:giftcard_pay_done,7:CardDelView,8:modifyCardStock)', max_length=2),
        ),
    ]
