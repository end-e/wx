# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/20 8:52'
import json,math
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View

from admin.models import GiftCard, GiftImg
from admin.utils.myClass import MyView
from admin.utils import method
from admin.forms import GiftCardForm

class CardView(View):
    def get(self, request):
        card_list = GiftCard.objects.values('id', 'wx_card_id', 'title', 'init_balance', 'price', 'quantity') \
            .filter(status='0')
        return render(request, 'giftcard/card_list.html', locals())


class CardEditView(MyView):
    def get(self, request, card_id):
        card_id = card_id
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        if card_id != '0':
            card = GiftCard \
                .objects \
                .values('id', 'title', 'background_pic', 'logo', 'init_balance', 'price', 'brand_name', 'quantity',
                        'status', 'max_give', 'notice', 'description', 'wx_card_id') \
                .get(id=card_id)

        return render(request, 'giftcard/card_edit.html', locals())

    def post(self, request, card_id):
        access_token = MyView().token
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        action = request.POST.get('action')
        if action == 'local':
            if card_id == '0':
                form = GiftCardForm(request.POST)
            else:
                qs_card = GiftCard.objects.get(pk=card_id)
                form = GiftCardForm(request.POST, instance=qs_card)
            if form.is_valid():
                form.save()
        elif action == 'wx':
            if card_id == '0':
                form = GiftCardForm(request.POST)
            else:
                qs_card = GiftCard.objects.get(pk=card_id)
                form = GiftCardForm(request.POST, instance=qs_card)
            if form.is_valid():
                # 处理本地数据
                qs_wx_card_id = form.cleaned_data['wx_card_id']
                res_save = form.save()
                # 上传微信
                if qs_wx_card_id:
                    # TODO 修改卡实例信息
                    url = 'https://api.weixin.qq.com/card/update?access_token={access_token}' \
                        .format(access_token=access_token)
                    data = method.createCardEditData(form)
                    data = json.dumps(data, ensure_ascii=False).encode('utf-8')

                    rep = requests.post(url, data=data)
                    rep_data = json.loads(rep.text)
                    res = {}
                    if rep_data['errmsg'] == 'ok':
                        res["status"] = 0
                    else:
                        res["status"] = 1
                        res["errcode"] = rep_data['errcode']
                        res["errmsg"] = rep_data['errmsg']

                else:
                    # TODO 新建卡实例信息
                    url = 'https://api.weixin.qq.com/card/create?access_token={access_token}' \
                        .format(access_token=access_token)
                    data = method.createCardData(form)
                    data = json.dumps(data, ensure_ascii=False).encode('utf-8')

                    response = requests.post(url, data=data)
                    res_data = json.loads(response.text)

                    msg = {}
                    if res_data['errmsg'] == 'ok':
                        wx_card_id = res_data['card_id']
                        if card_id == '0':
                            GiftCard.objects.filter(id=res_save.id).update(wx_card_id=wx_card_id)
                        else:
                            GiftCard.objects.filter(id=card_id).update(wx_card_id=wx_card_id)
                        msg['status'] = 0
                    else:
                        msg['status'] = 1
                        msg['text'] = res_data['errmsg']
                        msg['errcode'] = res_data['errcode']

        return render(request, 'giftcard/card_edit.html', locals())


class CardWxView(MyView):
    def get(self, request,page_num):
        count = 15
        page_num = int(page_num)
        offset = (page_num-1)*count
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/batchget?access_token={token}' \
            .format(token=access_token)
        data = {
            "offset": offset,
            "count": count,
            "status_list": ["CARD_STATUS_VERIFY_OK", "CARD_STATUS_DISPATCH"]
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        rep = requests.post(url, data=data)
        rep_data = json.loads(rep.text)
        total_num = rep_data['total_num']
        total_page = math.ceil(total_num/count)
        next_page = method.getNextPageNum2(page_num,total_num)
        prev_page = method.getPrePageNum2(page_num)

        card_id_list = rep_data['card_id_list']
        card_list = []
        for card_id in card_id_list:
            cardInfoClass = CardInfoWxView()
            cardInfo = cardInfoClass.get(card_id)
            cardInfo['card_id'] = card_id
            card_list.append(cardInfo)
        return render(request, 'giftcard/card_wx_list.html', locals())


class CardInfoWxView(MyView):
    def get(self,wx_card_id):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/get?access_token={token}' \
            .format(token=access_token)
        data = {"card_id": wx_card_id}
        data = json.dumps(data,ensure_ascii=False).encode('utf-8')

        rep = requests.post(url,data=data)
        rep_data = json.loads(rep.text)
        if rep_data['errmsg'] == 'ok':
            card = rep_data['card']

            return card


class CardDelView(MyView):
    def get(self, request,action, card_id):
        res = {}
        if action == 'wx':
            access_token = MyView().token
            url = 'https://api.weixin.qq.com/card/delete?access_token={token}' \
                .format(token=access_token)
            data = {"card_id": card_id}
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')

            rep = requests.post(url, data=data)
            rep_data = json.loads(rep.text)

            if rep_data['errmsg'] == 'ok':
                GiftCard.objects.filter(wx_card_id=card_id).update(wx_card_id='',status='1')
                res["status"] = 0
            else:
                res["status"] = 1
                res["errcode"] = rep_data['errcode']
                res["errmsg"] = rep_data['errmsg']
        elif action == 'local':
            try:
                GiftCard.objects.filter(id=card_id).delete()
                res["status"] = 0
            except Exception as e:
                print(e)
                res["status"] = 1
        return HttpResponse(json.dumps(res))
