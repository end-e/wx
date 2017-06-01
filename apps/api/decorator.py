# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/1 8:08'
from django.http import HttpResponse

import json, datetime, time

from api.method import md5


def signature(func):
    def wrapper(request, *args, **kwargs):
        flag = True
        request_time = request.GET.get('request_time', '')
        request_result = request.GET.get('request_result', '')
        if request_time == '' or request_result == '':
            flag = False
        else:
            time_now = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
            timeArray = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
            time_int = int(time.mktime(timeArray)) * 1000

            if time_int > int(request_time):
                flag = False
            else:
                current_result = md5(md5('ikg' + request_time) + 'wxapp')
                if request_result != current_result:
                    flag = False
        if not flag:
            return HttpResponse(json.dumps({'status': 1}))
        else:
            return func(request, *args, **kwargs)

    return wrapper

