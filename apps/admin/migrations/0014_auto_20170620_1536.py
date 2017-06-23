# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0013_auto_20170620_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('page_id', models.CharField(null=True, verbose_name='微信返回货架ID', max_length=128, blank=True)),
                ('title', models.CharField(max_length=12, verbose_name='货架名称')),
                ('banner_pic', models.CharField(max_length=128, verbose_name='banner图片')),
                ('categories', models.CharField(max_length=256, verbose_name='一级分类列表')),
            ],
            options={
                'verbose_name_plural': '货架',
                'db_table': 'gift_page',
                'verbose_name': '货架',
            },
        ),
        migrations.AlterModelOptions(
            name='giftcategory',
            options={'verbose_name_plural': '分类', 'verbose_name': '分类'},
        ),
        migrations.AlterModelOptions(
            name='giftimg',
            options={'verbose_name_plural': '图片素材', 'verbose_name': '图片素材'},
        ),
        migrations.AlterModelOptions(
            name='gifttheme',
            options={'verbose_name_plural': '主题', 'verbose_name': '主题'},
        ),
        migrations.AlterModelOptions(
            name='giftthemeitem',
            options={'verbose_name_plural': '主题-item', 'verbose_name': '主题-item'},
        ),
        migrations.AlterModelOptions(
            name='giftthemepicitem',
            options={'verbose_name_plural': '主题-picItem', 'verbose_name': '主题-picItem'},
        ),
        migrations.AlterField(
            model_name='gifttheme',
            name='category',
            field=models.SmallIntegerField(default=0, verbose_name='所属分类'),
        ),
    ]
