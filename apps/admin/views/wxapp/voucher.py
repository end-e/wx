import json, datetime,time

from django.shortcuts import render
from django.http import HttpResponse

from admin.utils import method
from wxapp.models import Voucher


def index(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')

    kwargs = {}

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    List = Voucher.objects.filter(**kwargs).order_by('voucher_no')

    return render(request, 'wxapp/voucher/index.html', locals())


def voucherEdit(request, voucher_id):
    voucher = []
    img_url = ''
    if voucher_id != '0':
        voucher = Voucher.objects.get(pk=voucher_id)
        if voucher.voucher_image != '':
            img_url =  voucher.voucher_image.url

    return render(request, 'wxapp/voucher/edit_page.html', {'voucher': voucher, 'img_url':img_url})


def voucherSave(request):
    voucher_id = request.POST.get('voucher_id', '')
    if voucher_id is None:
        voucher_id = ''
    voucher_no = request.POST.get('voucher_no', '')
    voucher_name = request.POST.get('voucher_name', '')
    unit_price = request.POST.get('unit_price', '')
    voucher_price = request.POST.get('voucher_price', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    voucher_image = request.FILES.get('voucher_image')
    if voucher_image == None:
        voucher_image = ''

    if voucher_id != '':
        result = Voucher.objects.get(pk=voucher_id)
        result.voucher_no = voucher_no
        result.voucher_name = voucher_name
        result.unit_price = unit_price
        result.voucher_price = voucher_price
        result.begin_date = begin_date
        result.end_date = end_date
        if voucher_image != '':
            result.voucher_image = voucher_image
        result.save()
    else:
        result = Voucher.objects.create(voucher_no=voucher_no,
                                        voucher_name=voucher_name,
                                        unit_price=unit_price,
                                        voucher_price=voucher_price,
                                        begin_date=begin_date,
                                        end_date=end_date,
                                        voucher_image=voucher_image)
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    List = Voucher.objects.all().order_by('voucher_no')
    return render(request, 'wxapp/voucher/index.html', locals())

