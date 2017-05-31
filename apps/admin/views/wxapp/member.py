import json, datetime, time
from django.http import HttpResponse
from admin.utils import method
from user.models import WechatMembers


def getInfo(request):
    openid = request.GET.get('openid', '')

    result_dict = {'status':1,'msg':[]}
    request_time = request.GET.get('request_time', '')
    request_result = request.GET.get('request_result', '')
    if request_time == '':
        return HttpResponse(json.dumps(result_dict), content_type="application/json")
    if request_result == '':
        return HttpResponse(json.dumps(result_dict), content_type="application/json")

    time_now = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(time_now, "%Y-%m-%d %H:%M:%S")
    time_int = int(time.mktime(timeArray))*1000

    if time_int > int(request_time):
        return HttpResponse(json.dumps(result_dict), content_type="application/json")

    current_result = method.md5(method.md5('ikg' + request_time) + 'wxapp')

    if request_result != current_result:
        return HttpResponse(json.dumps(result_dict), content_type="application/json")

    member = WechatMembers.objects.get(openid=openid)
    msg = {}
    if member:
        msg['id'] = str(member.id)
        msg['nikename'] = str(member.nikename)
        msg['sex'] = str(member.sex)
        msg['city'] = str(member.city)
        msg['country'] = str(member.country)
        msg['province'] = str(member.province)
        msg['openid'] = str(member.openid)
        msg['telphone'] = str(member.telphone)
        msg['attentiontime'] = str(member.attentiontime)
        msg['username'] = str(member.username)
        msg['membernumber'] = str(member.membernumber)

        result_dict['status'] = 0
        result_dict['msg'] = msg
    return HttpResponse(json.dumps(result_dict), content_type="application/json")
