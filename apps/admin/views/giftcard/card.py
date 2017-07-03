# -*-  coding:utf-8 -*-
from django.db import transaction

from api.models import LogWx

__author__ = ''
__date__ = '2017/6/20 8:52'
import json, math,datetime
import requests

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.core.cache import caches

from admin.models import GiftCard, GiftImg,GiftThemeItem, GiftCardCode
from admin.utils.myClass import MyView, MyException
from admin.utils import method
from utils import db
from admin.forms import GiftCardForm,GiftCardEditForm


class CardView(View):
    def get(self, request):
        card_list = GiftCard.objects.values('id', 'wx_card_id', 'title', 'init_balance', 'price', 'quantity')

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
                form = GiftCardEditForm(request.POST, instance=qs_card)
            if form.is_valid():
                form.save()
                return redirect(reverse('admin:giftcard:cards'))
        elif action == 'wx':
            qs_wx_card_id = request.POST.get('wx_card_id','')
            if qs_wx_card_id:
                qs_card = GiftCard.objects.get(pk=card_id)
                form = GiftCardEditForm(request.POST, instance=qs_card)
            else:
                if card_id == '0' :
                    form = GiftCardForm(request.POST)
                else:
                    qs_card = GiftCard.objects.get(pk=card_id)
                    form = GiftCardForm(request.POST, instance=qs_card)
            if form.is_valid():
                # 处理本地数据
                qs_wx_card_id = form.cleaned_data['wx_card_id']
                res_save = form.save()
                # 上传微信
                res = {}
                if qs_wx_card_id:
                    # TODO 修改卡实例信息
                    url = 'https://api.weixin.qq.com/card/update?access_token={access_token}' \
                        .format(access_token=access_token)
                    data = method.createCardEditData(form)
                    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
                    rep = requests.post(url, data=data)
                    rep_data = json.loads(rep.text)
                    if rep_data['errmsg'] == 'ok':
                        return redirect(reverse('admin:giftcard:cards'))
                    else:
                        res["status"] = 1
                        LogWx.objects.create(
                            type='3',
                            errmsg=rep_data['errmsg'],
                            errcode=rep_data['errcode']
                        )
                        return render(request, 'giftcard/card_edit.html', locals())
                else:
                    # TODO 新建卡实例信息
                    url = 'https://api.weixin.qq.com/card/create?access_token={access_token}' \
                        .format(access_token=access_token)
                    data = method.createCardData(form)
                    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
                    rep = requests.post(url, data=data)
                    rep_data = json.loads(rep.text)

                    if rep_data['errmsg'] == 'ok':
                        wx_card_id = rep_data['card_id']
                        if card_id == '0':
                            GiftCard.objects.filter(id=res_save.id).update(wx_card_id=wx_card_id,status='2')
                        else:
                            GiftCard.objects.filter(id=card_id).update(wx_card_id=wx_card_id,status='2')
                        return redirect(reverse('admin:giftcard:cards'))
                    else:
                        res["status"] = 1
                        return render(request, 'giftcard/card_edit.html', locals())




class CardWxView(MyView):
    def get(self, request, page_num):
        count = 10
        page_num = int(page_num)
        offset = (page_num - 1) * count
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
        total_page = math.ceil(total_num / count)
        next_page = method.getNextPageNum2(page_num, total_num)
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
    def get(self, wx_card_id):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/get?access_token={token}' \
            .format(token=access_token)
        data = {"card_id": wx_card_id}
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        rep = requests.post(url, data=data)
        rep_data = json.loads(rep.text)
        if rep_data['errmsg'] == 'ok':
            card = rep_data['card']

            return card


class CardDelView(MyView):
    def get(self, request, action, card_id):
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
                GiftCard.objects.filter(wx_card_id=card_id).update(wx_card_id='', status='1')
                GiftThemeItem.objects.filter(wx_card_id=card_id).delete()
                res["status"] = 0
            else:
                res["status"] = 1
                res["errcode"] = rep_data['errcode']
                res["errmsg"] = rep_data['errmsg']
        elif action == 'local':
            try:
                GiftCard.objects.filter(id=card_id).delete()
                GiftThemeItem.objects.filter(wx_card_id=card_id).delete()
                res["status"] = 0
            except Exception as e:
                print(e)
                res["status"] = 1
        return HttpResponse(json.dumps(res))


class CardUpCodeAutoView(MyView):
    def get(self, request, wx_card_id):
        access_token = MyView().token
        try:
            qs_card = GiftCard.objects.values('init_balance').filter(wx_card_id=wx_card_id).first()
            value = qs_card['init_balance']
            codes = method.getCardCode(value)
            data = {
                "card_id": wx_card_id,
                "code": codes
            }
            res = method.upCardCode(access_token,wx_card_id,data)
        except Exception as e :
            print(e)


class CardUpCodeManualView(MyView):
    def get(self, request, wx_card_id):

        return render(request,'giftcard/card_code_up.html',locals())

    def post(self,request, wx_card_id):
        action = request.POST.get('action','')
        qs_card = GiftCard.objects.values('id','init_balance','quantity').filter(wx_card_id=wx_card_id).first()
        value = qs_card['init_balance']
        quantity = int(qs_card['quantity'])
        card_id = qs_card['id']
        if action == 'query':
            starts = request.POST.getlist('start[]')
            ends = request.POST.getlist('end[]')
            card_code_list = []
            card_code_list_old = []

            for i in range(0,len(starts)):
                for code in range(int(starts[i]),int(ends[i])+1):
                    card_code_list_old.append(str(code))
                start = starts[i].strip()
                end = ends[i].strip()
                card_codes = method.getCardCode2(start,end,value,quantity)
                card_code_list.extend(card_codes)

            new= set(card_code_list)
            if new:
                codes_correct = json.dumps(card_code_list)
                codes_correct_num = len(card_code_list)
            old= set(card_code_list_old)
            code_err_list = [code for code in old if code not in new]
            if code_err_list:
                codes_error = json.dumps(code_err_list)
                codes_error_num = len(code_err_list)

            return render(request, 'giftcard/card_code_up.html', locals())
        elif action == 'upload' :
            access_token = MyView().token
            codes = request.POST.getlist('codes[]')
            res = {}
            if len(codes)>100 :
                res['status'] = 1
                res['msg'] = 'Code上传数量大于100'
                return HttpResponse(json.dumps(res))
            data = {
                "card_id": wx_card_id,
                "code": codes
            }
            res_upload = method.upLoadCardCode(access_token, wx_card_id, data)
            code_success = []
            code_fail = []
            code_duplicate = []
            if res_upload['status'] == 0:
                code_success = codes
            elif res_upload['status'] == 1:#code未全部上传成功，则查询上传成功的code
                res_check = method.checkCardCodeOnWx(access_token,data)
                if res_check['status'] == 0:
                    code_fail = res_check['not_exist_code']
                    code_success = res_check['exist_code']
                else:
                    res['status'] = 1
                    res['msg'] = 'Code未全部上传成功，查询上传状态失败'
                    return HttpResponse(json.dumps(res))
            elif res_upload['status'] == 2:#上传code存在重复数据
                code_success = res_upload['succ_code']
                code_duplicate = res_upload['duplicate_code']

            res['code_success'] = ','.join(code_success)
            res['code_success_num'] = len(code_success)
            res['code_fail'] = ','.join(code_fail)
            res['code_fail_num'] = len(code_fail)
            try:
                with transaction.atomic():
                    #存储wx_card_id与code的对应关系
                    codes = code_success+code_duplicate
                    mode_list = []
                    for code in codes:
                        item = GiftCardCode()
                        item.wx_card_id = wx_card_id
                        item.code = code
                        mode_list.append(item)
                    GiftCardCode.objects.bulk_create(mode_list)
                    #更新guest中code的状态
                    res_update1 = method.updateCardMode(codes)
                    if res_update1['status'] != 0:
                        raise MyException('successCode状态更新失败')

            except Exception as e:
                res['status'] = 2
                res['msg'] = 'Code线下数据处理失败'
                if hasattr(e, 'value'):
                    res['msg'] = e.value

            return HttpResponse(json.dumps(res))


class CardChangeCodeView(MyView):
    def get(self, request, wx_card_id):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/code/update?access_token={token}' \
            .format(token=access_token)
        data = {
            "code": "12345678",
            "card_id": "pFS7Fjg8kV1IdDz01r4SQwMkuCKc",
            "new_code": "3495739475"
        }


class CardChangeBalance(MyView):
    def get(self, request):
        #1、查询消费记录
        # conn = db.getMsSqlConn()
        conn_226 = db.getMsSqlConn22()
        start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        start = '2017-07-03 11:35:52'
        last_purchserial = caches['default'].get('wx_ikg_tempmsg_last_purchserial', '')
        if last_purchserial:
            whereStr = "a.PurchSerial> '{last_purchserial}'".format(last_purchserial=last_purchserial)
        else:
            whereStr = "a.PurchDateTime> '{start}'".format(start=start)

        sql_order = "SELECT a.detail, a.CardNo " \
              "FROM GuestPurch0 AS a,guest AS b, (SELECT cardno, MAX (purchserial) purchserial from GuestPurch0 GROUP BY cardno) AS c " \
              "WHERE " + whereStr + " AND a.cardno=b.cardno AND b.cardtype = 12 AND a.purchserial=c.purchserial ORDER BY a.PurchSerial "
        cur_226 = conn_226.cursor()
        cur_226.execute(sql_order)
        orders = cur_226.fetchall()
        #2、拼接wx_card_id
        for order in orders:
            qs_card = GiftCardCode.objects.values('wx_card_id').filter(code=order['CardNo']).first()
            order['wx_card_id'] = qs_card['wx_card_id']

        access_token = MyView().token
        for o in orders:
            url ='https://api.weixin.qq.com/card/generalcard/updateuser?access_token={token}' \
                .format(token=access_token)
            data = {
                "code": o['CardNo'].strip(),
                "card_id": o['wx_card_id'],
                "balance": float(o['detail'])
            }

            data = json.dumps(data,ensure_ascii=False).encode('utf-8')
            rep = requests.post(url,data=data)
            rep_data = json.loads(rep.text)
            if rep_data['errcode'] !=0:
                #TODO 记录错误日志
                pass


class CardModifyStockView(MyView):
    def post(self,request):
        access_token = MyView().token
        wx_card_id = request.POST.get('wx_card_id','')
        increase = request.POST.get('increase',0)
        reduce = request.POST.get('reduce',0)
        res_modify = method.modifyCardStock(access_token,wx_card_id,increase,reduce)

        return HttpResponse(json.dumps(res_modify))