import json, datetime
from django.http import HttpResponse
from wxapp.models import Voucher
from api.decorator import signature

@signature
def getVoucherList(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')
    voucher_price = request.GET.get('voucher_price', '')

    result_dict = {'status':1,'msg':[]}

    kwargs = {}

    kwargs.setdefault('begin_date__lte', datetime.datetime.now())
    kwargs.setdefault('end_date__gte', datetime.datetime.now())

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    if voucher_price != '':
        kwargs.setdefault('voucher_price', voucher_price)

    vouchers = Voucher.objects.filter(**kwargs).order_by('voucher_no')
    msg = []
    if vouchers:
        for item in vouchers:
            vardict = {}
            vardict['voucher_id'] = str(item.id)
            vardict['voucher_no'] = str(item.voucher_no)
            vardict['voucher_name'] = str(item.voucher_name)
            vardict['voucher_price'] = str(item.voucher_price)
            vardict['begin_date'] = str(item.begin_date.strftime("%Y-%m-%d"))
            vardict['end_date'] = str(item.end_date.strftime("%Y-%m-%d"))
            vardict['voucher_image'] = 'https://www.zisai.net/media/' + str(item.voucher_image)
            msg.append(vardict)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")

@signature
def getVoucherInfo(request):
    voucher_id = request.GET.get('voucher_id', '')

    result_dict = {'status':1,'msg':[]}
    voucher = Voucher.objects.get(pk=voucher_id)
    msg = {}
    if voucher:
        msg['id'] = str(voucher.id)
        msg['voucher_no'] = str(voucher.voucher_no)
        msg['voucher_name'] = str(voucher.voucher_name)
        msg['voucher_price'] = str(voucher.voucher_price)
        msg['begin_date'] = str(voucher.begin_date.strftime("%Y-%m-%d"))
        msg['end_date'] = str(voucher.end_date.strftime("%Y-%m-%d"))
        msg['voucher_image'] = 'https://www.zisai.net/media/' + str(voucher.voucher_image)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")
