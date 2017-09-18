# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/9/16 11:01'
import json,datetime,math

from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.views.generic.base import View

from admin.models import  GiftOrder, GiftOrderInfo,GiftCardCode
from admin.forms import GiftRefundForm
from admin.utils.myClass import MyView,MyException
from admin.utils import method
from utils import giftcard,data
from api.views import cron

class OrderView(MyView):
    def get(self,request):
        page_num = 1
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        return render(request,'giftcard/order_list.html',locals())
    def post(self,request):
        access_token = MyView().token

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        begin = request.POST.get('begin')
        begin_time = method.getTimeStamp(begin+' 00:00:00')
        end = request.POST.get('end')
        end_time = method.getTimeStamp(end+' 23:59:59')
        page_num = int(request.POST.get('page_num', 1))
        count = int(request.POST.get('count', 10))
        offset = (page_num - 1) * count
        if not offset:
            offset = 0

        rep_data = giftcard.order_batchget(access_token,begin_time,end_time,offset,count)
        if rep_data['errmsg'] == 'ok':
            total_count = rep_data['total_count']
            total_page = math.ceil(total_count/count)
            next_page = method.getNextPageNum2(page_num, total_count)
            prev_page = method.getPrePageNum2(page_num)
            order_list = rep_data['order_list']

        else:
            errcode = rep_data['errcode']
            errmsg = rep_data['errmsg']

        return render(request, 'giftcard/order_list.html',locals())


class OrderRefundView(View):
    def get(self,request):
        return render(request,'giftcard/order_refund.html')

    @transaction.atomic
    def post(self,request):
        form = GiftRefundForm(request.POST)
        if form.is_valid():
            trans_id = form.cleaned_data['trans_id']
            qs_order = GiftOrder.objects.values('order_id','id').filter(trans_id=trans_id,refund='0')

            if qs_order.first():
                order = qs_order.first()
                qs_card = GiftOrderInfo.objects.values('code').filter(order_id=order['id'])
                code_list = [card['code'] for card in qs_card]
                try:
                    cards = data.getCardsBalance(code_list)
                    for card in cards:
                        if card['Detail'] != card['New_amount']:
                            raise MyException('卡号：' + card['cardNo'] + ',已存在消费')
                    with transaction.atomic():
                        #保存log
                        form.save()
                        #更新订单状态
                        qs_order.update(refund='1')
                        #更新卡状态
                        res_code = GiftCardCode.objects.filter(code__in=code_list).update(status='0')
                        if res_code != len(code_list):
                            raise MyException('card_code中状态更新失败')
                        res_guest = method.updateCardMode(code_list,1,9)
                        if res_guest['status'] == 1:
                            raise MyException('Guest中状态更新失败')

                        #调用退款接口
                        order_id = order['order_id']
                        access_token = MyView().token
                        rep_data = giftcard.oderRefund(access_token,order_id)

                        if rep_data['errcode'] == 0:
                            res = method.createResult(0,'ok')
                        else:
                            raise MyException(rep_data['errmsg'])
                except Exception as e:
                    print(e)
                    msg =e.value if hasattr(e, 'value') else e.args[0]
                    res = method.createResult(2, msg)
            else:
                res = method.createResult(1, 'trans_id is not exist')

        return render(request, 'giftcard/order_refund.html', locals())


class OrderCompareView(View):
    def get(self,request):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        return render(request,'giftcard/order_compare.html',locals())
    def post(self,request):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        begin = request.POST.get('begin',today)
        end = request.POST.get('end',today)

        begin_time = method.getTimeStamp(begin + ' 00:00:00')
        end_time = method.getTimeStamp(end + ' 23:59:59')

        res = {}
        res['status'] = 0
        res_compare = cron.gift_compare_order(begin_time,end_time)
        if res_compare['status'] == 0:
            res = method.createResult(0,'ok')
        else:
            res = method.createResult(1, 'fail')

        return HttpResponse(json.dumps(res))
