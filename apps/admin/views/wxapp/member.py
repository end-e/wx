import json
from django.http import HttpResponse
from user.models import WechatMembers

def getInfo(request):
    openid = request.GET.get('openid', '')

    member = WechatMembers.objects.get(openid=openid)
    msg={}
    if member:
        msg['id']= str(member.id)
        msg['nikename']= str(member.nikename)
        msg['sex']= str(member.sex)
        msg['city']= str(member.city)
        msg['country']= str(member.country)
        msg['province']= str(member.province)
        msg['openid']= str(member.openid)
        msg['telphone']= str(member.telphone)
        msg['attentiontime']= str(member.attentiontime)
        msg['username']= str(member.username)
        msg['membernumber']= str(member.membernumber)

    return HttpResponse(json.dumps(msg), content_type="application/json")