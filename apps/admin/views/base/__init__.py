# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/25 11:59'
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request, '', locals())