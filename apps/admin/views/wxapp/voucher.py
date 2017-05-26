from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic.base import View
import datetime, pymssql, json
from admin.utils import method
from admin.forms import UserForm
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
    voucher_no = request.POST.get('voucher_no', '')
    voucher_name = request.POST.get('voucher_name', '')
    voucher_price = request.POST.get('voucher_price', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')

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
    return vouchers


def getVoucherInfo(request):
    voucher_id = request.POST.get('voucher_id', '')

    voucher = Voucher.objects.get(pk=voucher_id)
    return voucher