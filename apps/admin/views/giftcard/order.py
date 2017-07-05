# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/21 10:00'
import json,requests,math

from django.shortcuts import render

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
