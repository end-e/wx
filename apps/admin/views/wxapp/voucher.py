import json

from django.shortcuts import render
from django.http import HttpResponse

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
    if voucher_id != '0':
        voucher = Voucher.objects.get(pk=voucher_id)
    return render(request, 'wxapp/voucher/edit_page.html', {'voucher': voucher})

def voucherSave(request):
    voucher_id = request.POST.get('voucher_id', '')
    if voucher_id is None:
        voucher_id = ''
    voucher_no = request.POST.get('voucher_no', '')
    voucher_name = request.POST.get('voucher_name', '')
    voucher_price = request.POST.get('voucher_price', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    voucher_image = request.POST.get('voucher_image', '')
    if voucher_id != '':
        result = Voucher.objects.get(pk=id).update(voucher_no=voucher_no,
                                                   voucher_name=voucher_name,
                                                   voucher_price=voucher_price,
                                                   begin_date=begin_date,
                                                   end_date=end_date,
                                                   voucher_image=voucher_image)
    else:
        result = Voucher.objects.create(voucher_no=voucher_no,
                                        voucher_name=voucher_name,
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

def getVoucherList(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')
    voucher_price = request.GET.get('voucher_price', '')
    begin_date = request.GET.get('begin_date', '')
    end_date = request.GET.get('end_date', '')

    kwargs = {}

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    if voucher_price != '':
        kwargs.setdefault('voucher_price', voucher_price)

    if begin_date != '':
        kwargs.setdefault('begin_date', begin_date)

    if end_date != '':
        kwargs.setdefault('end_date', end_date)

    vouchers = Voucher.objects.filter(**kwargs).order_by('voucher_no')
    msg ={}
    vardict = {}
    if vouchers:
        for item in vouchers:
            vardict['voucher_no'] = str(item.voucher_no)
            vardict['voucher_name'] = str(item.voucher_name)
            vardict['voucher_price'] = str(item.voucher_price)
            vardict['begin_date'] = str(item.begin_date)
            vardict['end_date'] = str(item.end_date)
            vardict['voucher_image'] = str(item.voucher_image)
            msg[str(item.id)]= vardict
    return HttpResponse(json.dumps(msg), content_type="application/json")


def getVoucherInfo(request):
    voucher_id = request.GET.get('voucher_id', '')

    voucher = Voucher.objects.get(pk=voucher_id)
    msg={}
    if voucher:
        msg['id']= str(voucher.id)
        msg['voucher_no']= str(voucher.voucher_no)
        msg['voucher_name']= str(voucher.voucher_name)
        msg['voucher_price']= str(voucher.voucher_price)
        msg['begin_date']= str(voucher.begin_date)
        msg['end_date']= str(voucher.end_date)
        msg['voucher_image']= str(voucher.voucher_image)

    return HttpResponse(json.dumps(msg), content_type="application/json")