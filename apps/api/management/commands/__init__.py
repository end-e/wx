# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/4/19 14:39'
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request, '', locals())