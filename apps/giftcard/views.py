import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from giftcard import Event
from admin.models import GiftOrder
from utils import wx

@csrf_exempt
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
        event = xml.find('Event').text
        if event == 'giftcard_pay_done':
            # 购买付款成功--TODO 本地存储订单
            orderId = xml.find('OrderId').text
            order = GiftOrder.objects.filter(order_id=orderId)
            httpResponse = HttpResponse()
            httpResponse.status_code = 200
            flag = True
            if order.count()==0:
                res = Event.giftcard_pay_done(orderId)
                if res['status'] != 0:
                    flag= False
            return wx.respondToWx(flag)

        elif event == 'giftcard_user_accept':
            # 用户领取礼品卡成功
            return wx.respondToWx(True)
        elif event == 'card_pass_check':
            # 审核通过--TODO 上传自定义CODE
            #礼品卡免审，此处跳过
            # cardid = xml.find('CardId').text
            # kwargs = {'wx_card_id':cardid}
            # return redirect(reverse('admin:giftcard:card_code_upload_auto', kwargs=kwargs))
            return wx.respondToWx(True)

        elif event == 'user_gifting_card':
            #转增后更改code
            cardid = xml.find('CardId').text
            # kwargs = {'wx_card_id': cardid}
            # res = Event.user_gifting_card
            return wx.respondToWx(True)
        elif event == 'user_del_card':
            open_id = xml.find('FromUserName').text
            card_id = xml.find('CardId').text
            return wx.respondToWx(True)
        elif event == 'giftcard_send_to_friend':
            return wx.respondToWx(True)
        else:
            return wx.respondToWx(True)