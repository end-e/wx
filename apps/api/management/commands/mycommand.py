# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/4/19 14:39'
from django.core.management.base import BaseCommand
from api.models import AccessToken
import datetime,logging

class Command(BaseCommand):
    def handle(self, *args, **options):
        a = AccessToken.objects.create(
            add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            access_token='132123',
            expires_in='7200',
        )