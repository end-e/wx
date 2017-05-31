# -*- coding: utf-8 -*-
from django.shortcuts import render
from wechatpy import parse_message


def switch_type(request):
    xml = request.POST
    msg = parse_message(xml)
    print(msg.type)
