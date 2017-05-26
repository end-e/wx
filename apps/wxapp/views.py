from django.shortcuts import render
from django.http import HttpResponse
from wxapp.models import Voucher

def index(request):
    return HttpResponse('ceshi jietong')


def getList(kwargs):
    List = Voucher.objects.filter(**kwargs)
    return List


def getInfo(kwarg):
    voucher = Voucher.objects.get(voucher_no=kwarg)
    return voucher