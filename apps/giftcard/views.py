import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from api.models import Log


def conn(request):
    if request.method == 'GET':

        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        token = 'giftcard'
        try:
            check_signature(token, signature, timestamp, nonce)
            return HttpResponse(echostr)
        except InvalidSignatureException:
            return HttpResponse(u'验证失败')


    elif request.method == 'POST':
        xml = request.body
        xml = ET.fromstring(xml)

        app_id = xml.find('ToUserName').text
        event = xml.find('Event').text
        if event == 'giftcard_pay_done':# 购买付款成功
            #TODO 更改ERP内的卡状态
            pass
        elif event == 'giftcard_user_accept':
            # TODO 用户领取礼品卡成功
            pass
        elif event == 'card_pass_check':# 审核通过
            # TODO 上传自定义CODE

            cardid = xml.find('CardId').text
            Log.objects.create(
                open_id='审核通过',
                errmsg=cardid,
                errcode=cardid,
                type='99',
            )
            kwargs = {'wx_card_id':cardid}
            return redirect(reverse('admin:giftcard:card_code_upload_auto', kwargs=kwargs))
        elif event == 'user_gifting_card':
            cardid = xml.find('CardId').text
            kwargs = {'wx_card_id': cardid}
            return redirect(reverse('admin:giftcard:card_code_change', kwargs=kwargs))
        elif event == 'user_del_card':
            open_id = xml.find('FromUserName').text
            card_id = xml.find('CardId').text

