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
    voucher_price = request.POST.get('voucher_price', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    voucher_image = request.FILES.get('voucher_image')
    if voucher_image == None:
        voucher_image = ''

    if voucher_id != '':
        if voucher_image != '':
            result = Voucher.objects.filter(pk=voucher_id).update(voucher_no=voucher_no,
                                                       voucher_name=voucher_name,
                                                       voucher_price=voucher_price,
                                                       begin_date=begin_date,
                                                       end_date=end_date,
                                                       voucher_image=voucher_image)
        else:
            result = Voucher.objects.filter(pk=voucher_id).update(voucher_no=voucher_no,
                                                       voucher_name=voucher_name,
                                                       voucher_price=voucher_price,
                                                       begin_date=begin_date,
                                                       end_date=end_date)
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


# def getVoucherList(request):
#     voucher_no = request.GET.get('voucher_no', '')
#     voucher_name = request.GET.get('voucher_name', '')
#     voucher_price = request.GET.get('voucher_price', '')
#
#     result_dict = {'status':1,'msg':[]}
#     request_time = request.GET.get('request_time', '')
#     request_result = request.GET.get('request_result', '')
#     if request_time == '':
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#     if request_result == '':
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     time_now = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
#     timeArray = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
#     time_int = int(time.mktime(timeArray))*1000
#
#     if time_int > int(request_time):
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     current_result = method.md5(method.md5('ikg' + request_time) + 'wxapp')
#
#     if request_result != current_result:
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     kwargs = {}
#
#     kwargs.setdefault('begin_date__lte', datetime.datetime.now())
#     kwargs.setdefault('end_date__gte', datetime.datetime.now())
#
#     if voucher_no != '':
#         kwargs.setdefault('voucher_no__contains', voucher_no)
#
#     if voucher_name != '':
#         kwargs.setdefault('voucher_name__contains', voucher_name)
#
#     if voucher_price != '':
#         kwargs.setdefault('voucher_price', voucher_price)
#
#     vouchers = Voucher.objects.filter(**kwargs).order_by('voucher_no')
#     msg = []
#     if vouchers:
#         for item in vouchers:
#             vardict = {}
#             vardict['voucher_id'] = str(item.id)
#             vardict['voucher_no'] = str(item.voucher_no)
#             vardict['voucher_name'] = str(item.voucher_name)
#             vardict['voucher_price'] = str(item.voucher_price)
#             vardict['begin_date'] = str(item.begin_date.strftime("%Y-%m-%d"))
#             vardict['end_date'] = str(item.end_date.strftime("%Y-%m-%d"))
#             vardict['voucher_image'] = 'https://www.zisai.net/media/' + str(item.voucher_image)
#             msg.append(vardict)
#
#         result_dict['status'] = 0
#         result_dict['msg'] = msg
#
#     return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#
# def getVoucherInfo(request):
#     voucher_id = request.GET.get('voucher_id', '')
#
#     result_dict = {'status':1,'msg':[]}
#     request_time = request.GET.get('request_time', '')
#     request_result = request.GET.get('request_result', '')
#     if request_time == '':
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#     if request_result == '':
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     time_now = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
#     timeArray = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
#     time_int = int(time.mktime(timeArray))*1000
#
#     if time_int > int(request_time):
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     current_result = method.md5(method.md5('ikg' + request_time) + 'wxapp')
#
#     if request_result != current_result:
#         return HttpResponse(json.dumps(result_dict), content_type="application/json")
#
#     voucher = Voucher.objects.get(pk=voucher_id)
#     msg = {}
#     if voucher:
#         msg['id'] = str(voucher.id)
#         msg['voucher_no'] = str(voucher.voucher_no)
#         msg['voucher_name'] = str(voucher.voucher_name)
#         msg['voucher_price'] = str(voucher.voucher_price)
#         msg['begin_date'] = str(voucher.begin_date.strftime("%Y-%m-%d"))
#         msg['end_date'] = str(voucher.end_date.strftime("%Y-%m-%d"))
#         msg['voucher_image'] = 'https://www.zisai.net/media/' + str(voucher.voucher_image)
#
#         result_dict['status'] = 0
#         result_dict['msg'] = msg
#
#     return HttpResponse(json.dumps(result_dict), content_type="application/json")
