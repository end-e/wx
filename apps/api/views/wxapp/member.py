import json
from django.http import HttpResponse
from user.models import WechatMembers
from api.decorator import signature

@signature
def getInfo(request):
    openid = request.GET.get('openid', '')

    result_dict = {'status':1,'msg':[]}

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
