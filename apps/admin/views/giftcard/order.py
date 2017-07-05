# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/21 10:00'
import json,requests,math

from django.shortcuts import render
from django.db import transaction

from admin.models import GiftCardCode,GiftOrder,GiftOrderInfo
from api.models import LogWx
from admin.utils.myClass import MyView
from admin.utils import method

class OrderView(MyView):
    def get(self,request):

        return render(request,'giftcard/order_list.html',locals())
    def post(self,request):
        access_token = MyView().token
        url = "https://api.weixin.qq.com/card/giftcard/order/batchget?access_token={access_token}" \
            .format(access_token=access_token)
        begin = request.POST.get('begin_time')
        begin_time = method.getTimeStamp(begin+' 00:00:00')
        end = request.POST.get('end_time')
        end_time = method.getTimeStamp(end+' 23:59:59')
        count = 10
        page_num = request.POST.get('page_num',1)
        page_num = int(page_num)
        offset = (page_num - 1) * count
        if not offset:
            offset = 0
        data = {
            "begin_time": begin_time,
            "end_time": end_time,
            "sort_type": "ASC",
            "offset": offset,
            "count": count
        }
        data = json.dumps(data,ensure_ascii=False).encode('utf-8')
        rep = requests.post(url,data=data)
        rep_data = json.loads(rep.text)
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


class OrderLocalCreateView(MyView):
    def get(self,request,order_id):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/giftcard/order/get?access_token={token}'\
            .format(token=access_token)
        data = { "order_id": order_id }
        data = json.dumps(data,ensure_ascii=False).encode('utf-8')
        rep = requests.post(url, data=data)
        rep_data = json.loads(rep.text)
        if rep_data['errcode'] == 0:
            order = rep_data['order']
            card_list = order['card_list']
            try:
                with transaction.atomic():
                    order = GiftOrder.objects.create(
                        order_id=order['order_id'],trans_id=order['trans_id'],
                        create_time=order['create_time'],pay_finish_time=order['pay_finish_time'],
                        total_price=order['create_time'],open_id=order['pay_finish_time'],
                        accepter_openid=order['accepter_openid']
                    )
                    orderID = order.id
                    info_list = []
                    code_list = []
                    for card in card_list:
                        card_list.append(card['code'])
                        info = GiftOrderInfo()
                        info['order_id'] = orderID
                        info['card_id'] = card['card_id']
                        info['price'] = card['price']
                        info['code'] = card['code']
                        info_list.append(info)
                    GiftOrderInfo.objects.bulk_create(info_list)
                    GiftCardCode.objects.filter(code__in=code_list).update(status='1')
            except:
                LogWx.objects.create(
                    type='6',
                    errmsg='推送事件giftcard_pay_done，触发本地数据存储失败',
                    errcode='',
                    remark='wx_order_id:{order}'.format(order=order_id)
                )
        else:
            LogWx.objects.create(
                type='6',
                errmsg=rep_data['errmsg'],
                errcode=rep_data['errcode'],
                remark='wx_order_id:{order}'.format(order=order_id)
            )