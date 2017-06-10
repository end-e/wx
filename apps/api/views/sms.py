# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/23 15:59'
import json
import random

from django.core.cache import caches
from django.http import HttpResponse

import utils.SmsSender as SmsSender


def main(request):
    # 请根据实际 appid 和 appkey 进行开发，以下只作为演示 sdk 使用
    appid = 1400029439
    appkey = "7cd51448bff9529d03f9dddb562ae5b0"
    phone = request.POST.get('phone','')

    msg = {}
    if phone:
        single_sender = SmsSender.SmsSingleSender(appid, appkey)
        sms_code = random.randint(1,9999)
        sms_msg = "【宽广超市】尊敬的顾客：你的验证码是"+str(sms_code)
        res = single_sender.send(0, "86", phone, sms_msg, "", "")
        res = json.loads(res.decode())
        if(res['result'] == 0):
            caches['default'].set('sms_'+str(phone),sms_code,30*60)
            msg['status'] = 0
        else:
            #发送失败
            msg['status'] = 1
    else:
        #手机号为空
        msg['status'] = 2

    return HttpResponse(json.dumps(msg))

    # # 指定模板单发
    # params = ["指定模板单发", "深圳", "小明"]
    # result = single_sender.send_with_param("86", phone_number, templ_id, params, "", "", "")
    # rsp = json.loads(result)
    # print(result)


# if __name__ == "__main__":
#     main()
