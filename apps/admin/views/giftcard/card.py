# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/20 8:52'
import json, math, time, requests

from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.views.generic.base import View
from django.db.models import Count, F

from admin.models import GiftCard, GiftImg, GiftTheme, GiftThemeItem, GiftCardCode, GiftOrder, GiftOrderInfo
from admin.utils.myClass import MyView, MyException
from admin.utils import method
from utils import data,giftcard
from admin.forms import GiftCardForm, GiftCardEditForm
from api.models import LogWx


class CardView(View):
    def get(self, request):
        card_list = GiftCard.objects.values('id', 'name', 'wx_card_id', 'title', 'init_balance', 'price', 'quantity',
                                            'status') \
            .order_by('-status', '-id')

        for card in card_list:
            qs_code = GiftCardCode.objects.filter(wx_card_id=card['wx_card_id'])
            card['stock'] = qs_code.filter(status='0').count()
            if qs_code.filter(status='1'):
                card['die'] = 1

        return render(request, 'giftcard/card_list.html', locals())


class CardEditView(MyView):
    def get(self, request, card_id):
        card_id = card_id
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        if card_id != '0':
            card = GiftCard.objects \
                .values('id', 'name', 'title', 'background_pic', 'logo', 'init_balance', 'price', 'brand_name',
                        'quantity',
                        'status', 'max_give', 'notice', 'description', 'wx_card_id') \
                .get(id=card_id)

        return render(request, 'giftcard/card_edit.html', locals())

    def post(self, request, card_id):
        access_token = MyView().token
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        action = request.POST.get('action')
        res = {}
        res['status'] = 0
        # 本地暂存
        if action == 'local':
            wx_card_id = request.POST.get('wx_card_id', '')
            if wx_card_id:
                qs_card = GiftCard.objects.get(pk=card_id)
                form = GiftCardEditForm(request.POST, instance=qs_card)
            else:
                if card_id == '0':
                    form = GiftCardForm(request.POST)
                else:
                    qs_card = GiftCard.objects.get(pk=card_id)
                    form = GiftCardForm(request.POST, instance=qs_card)
            if form.is_valid():
                try:
                    res_save = form.save()
                except Exception as e:
                    res['status'] = 1
                    LogWx.objects.create(type='3', errmsg=e, errcode='3')
            else:
                res['status'] = 1

            return render(request, 'giftcard/card_edit.html', locals())
        # 直接上传微信
        elif action == 'wx':
            wx_card_id = request.POST.get('wx_card_id', '')
            if wx_card_id:
                qs_card = GiftCard.objects.get(pk=card_id)
                form = GiftCardEditForm(request.POST, instance=qs_card)
            else:
                if card_id == '0':
                    form = GiftCardForm(request.POST)
                else:
                    qs_card = GiftCard.objects.get(pk=card_id)
                    form = GiftCardForm(request.POST, instance=qs_card)
            if form.is_valid():
                # 处理本地数据
                wx_card_id = form.cleaned_data['wx_card_id']
                try:
                    res_save = form.save()
                except Exception as e:
                    res['status'] = 1
                    LogWx.objects.create(type='3', errmsg=e, errcode='3')
                    return render(request, 'giftcard/card_edit.html', locals())

                # 上传微信
                if wx_card_id:
                    # TODO 修改卡实例信息
                    url = 'https://api.weixin.qq.com/card/update?access_token={access_token}' \
                        .format(access_token=access_token)
                    data = method.createCardEditData(form)
                    data = json.dumps(data, ensure_ascii=False).encode('utf-8')
                    rep = requests.post(url, data=data)
                    rep_data = json.loads(rep.text)
                    if rep_data['errmsg'] != 'ok':
                        res["status"] = 1
                        LogWx.objects.create(type='3', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
                                             remark='wx_card_id:{id}'.format(id=wx_card_id))
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
                        try:
                            if card_id == '0':
                                GiftCard.objects.filter(id=res_save.id).update(wx_card_id=wx_card_id, status='9')
                            else:
                                GiftCard.objects.filter(id=card_id).update(wx_card_id=wx_card_id, status='9')
                        except Exception as e:
                            res["status"] = 1
                            LogWx.objects.create(type='3', errmsg=e, errcode='3')
                    else:
                        res["status"] = 1
                        LogWx.objects.create(type='3', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'])
                    return render(request, 'giftcard/card_edit.html', locals())


class CardInfoView(MyView):
    def get(self, request, card_id):
        card = GiftCard.objects \
            .values('id', 'name', 'title', 'background_pic', 'logo', 'init_balance', 'price', 'brand_name', 'quantity',
                    'status', 'max_give', 'notice', 'description', 'wx_card_id') \
            .get(id=card_id)

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
        try:
            total_page, next_page, prev_page = 1, 1, 1
            rep = requests.post(url, data=data, verify=False)
            rep_data = json.loads(rep.text)

            if rep_data['errcode'] == 0:
                total_num = rep_data['total_num']
                total_page = math.ceil(total_num / count)
                next_page = method.getNextPageNum2(page_num, total_num)
                prev_page = method.getPrePageNum2(page_num)

                card_id_list = rep_data['card_id_list']
                card_list = []
                for card_id in card_id_list:
                    cardInfoClass = CardInfoWxView()
                    cardInfo = cardInfoClass.get(card_id)
                    card_list.append(cardInfo)

            else:
                LogWx.objects.create(type='98', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'])
        except requests.exceptions.ConnectionError as e:
            print(e)
            time.sleep(5)
            self.get(request, page_num)

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
            item = {}
            item['wx_card_id'] = wx_card_id
            item['title'] = card['general_card']['base_info']['title']
            item['total_quantity'] = card['general_card']['base_info']['sku']['total_quantity']
            item['quantity'] = card['general_card']['base_info']['sku']['quantity']
            item['price'] = card['general_card']['base_info']['giftcard_info']['price']
            item['init_balance'] = card['general_card']['init_balance']
            return item
        else:
            LogWx.objects.create(type='99', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'])


class CardStockView(View):
    def get(self, request):
        themes = GiftTheme.objects.values('name', 'id').filter(status='0')
        return render(request, 'giftcard/card_stock.html', locals())

    def post(self, request):
        themes = GiftTheme.objects.values('name', 'id').filter(status='0')
        name = request.POST.get('name', '')
        balance = request.POST.get('balance', '')
        theme_id = int(request.POST.get('theme', ''))
        kwargs = {}
        if name:
            kwargs.setdefault('name', name)
        if balance:
            kwargs.setdefault('init_balance', balance)
        card_ids = []
        cards = []
        if theme_id:
            items = GiftThemeItem.objects.values('wx_card_id').filter(theme_id=theme_id)
            if items.exists():
                card_ids = [item['wx_card_id'] for item in items]
                kwargs.setdefault('wx_card_id__in', card_ids)
                cards = GiftCard.objects.filter(**kwargs).values('name', 'title', 'init_balance', 'price', 'wx_card_id')
        else:
            cards = GiftCard.objects.filter(**kwargs).values('name', 'title', 'init_balance', 'price', 'wx_card_id')
            card_ids = [card['wx_card_id'] for card in cards]

        stocks = GiftCardCode.objects.values('wx_card_id', 'status').filter(wx_card_id__in=card_ids) \
            .annotate(stock=Count('code'))

        for card in cards:
            for stock in stocks:
                if card['wx_card_id'] == stock['wx_card_id']:
                    if 'stock' in card:
                        card['stock'] += stock['stock']
                    else:
                        card['stock'] = stock['stock']

                    if stock['status'] == '0':
                        if 'stock_now' in card:
                            card['stock_now'] += stock['stock']
                        else:
                            card['stock_now'] = stock['stock']
        return render(request, 'giftcard/card_stock.html', locals())


class CardDelView(MyView):
    @transaction.atomic
    def post(self, request):
        res = {"status": 0}
        action = request.POST.get('action')
        wx_card_id = request.POST.get('wx_card_id')
        status = request.POST.get('status')
        access_token = MyView().token
        if action == 'wx':
            try:
                with transaction.atomic():
                    qs_card_codes = GiftCardCode.objects.filter(wx_card_id=wx_card_id, status='0')
                    if qs_card_codes.exists():
                        cards = qs_card_codes.values('code', 'wx_card_id')
                        codes_delete = self.getDeleteCodes(access_token, cards)
                        if codes_delete < cards.count():
                            raise MyException('此卡已经存在销售记录，禁止删除！')
                        else:
                            # 1.0更新线下card信息
                            GiftCard.objects.filter(wx_card_id=wx_card_id).update(wx_card_id='', status=status)
                            # 1.1删除主题下的此卡
                            GiftThemeItem.objects.filter(wx_card_id=wx_card_id).delete()
                            # 1.2处理未出售的code
                            qs_card_codes.delete()
                            res_mssql = method.updateCardMode(codes_delete, 1, 9)
                            if res_mssql['status'] != 0:
                                raise MyException('Code状态更新失败')
                            # 2、处理线上业务流程
                            delete = self.deleteCard(access_token, wx_card_id, action)
                            if not delete:
                                res["status"] = 2
                    else:
                        # 1.0更新线下card信息
                        GiftCard.objects.filter(wx_card_id=wx_card_id).update(wx_card_id='', status=status)
                        # 1.1删除主题下的此卡
                        GiftThemeItem.objects.filter(wx_card_id=wx_card_id).delete()
                        delete = self.deleteCard(access_token,wx_card_id,action)
                        if not delete:
                            res["status"] = 2
            except Exception as e:
                res["status"] = 1
                LogWx.objects.create(
                    type='7', errmsg=e, errcode='7',
                    remark='wx_card_id:{card},action:{action}'.format(card=wx_card_id, action=action)
                )
        elif action == 'local':
            try:
                with transaction.atomic():
                    if status == '0':
                        # 1更新卡状态
                        GiftCard.objects.filter(wx_card_id=wx_card_id).update(status=status)
                        # 删除主题下对应的卡
                        GiftThemeItem.objects.filter(wx_card_id=wx_card_id).delete()
                        # 2处理未出售的code
                        qs_card_codes = GiftCardCode.objects.filter(wx_card_id=wx_card_id, status='0')
                        if qs_card_codes.exists():
                            cards = qs_card_codes.values('','code')
                            codes_delete = self.getDeleteCodes(access_token, cards)

                            # 2.1删除gift_card_code中对应的code
                            qs_card_codes.filter(code__in=codes_delete).delete()
                            # 2.2更新guest的mode
                            res_mssql = method.updateCardMode(codes_delete, 1, 9)
                            if res_mssql['status'] != 0:
                                raise MyException('Code状态更新失败')
                    elif status in ('1', '2'):
                        # 1删除主题下的此卡
                        GiftCard.objects.filter(id=wx_card_id).update(status=status)
                        GiftThemeItem.objects.filter(wx_card_id=wx_card_id).delete()
                res["status"] = 0
            except Exception as e:
                print(e)
                res["status"] = 1
        return HttpResponse(json.dumps(res))

    def deleteCard(self,access_token, wx_card_id, action):
        rep_data = giftcard.deleteCard(access_token, wx_card_id)
        if rep_data['errmsg'] != 'ok':
            LogWx.objects.create(
                type='7', errmsg=rep_data['errmsg'], errcode=rep_data['errcode'],
                remark='wx_card_id:{card},action:{action}'.format(card=wx_card_id, action=action)
            )
            return False
        else:
            return True

    def getDeleteCodes(self,access_token, cards):
        code_delete = []
        for card in cards:
            rep_card = giftcard.getCardCodeInfo(access_token, card['wx_card_id'], card['code'])
            if rep_card['errmsg'] == 'ok':
                rep_order = giftcard.getOrder(access_token, rep_card['order_id'])
                if rep_order['errmsg'] == 'ok':
                    data.saveAndUpdateLocalData(rep_order['order'])
            else:
                code_delete.append(card['code'])
        return code_delete


class CardUpCodeManualView(View):
    def get(self, request, wx_card_id):
        card = GiftCard.objects.values('price', 'name').get(wx_card_id=wx_card_id)
        price = card['price']
        return render(request, 'giftcard/card_code_up.html', locals())

    @transaction.atomic
    def post(self, request, wx_card_id):
        action = request.POST.get('action', '')
        qs_card = GiftCard.objects.values('id', 'init_balance', 'quantity').filter(wx_card_id=wx_card_id).first()
        value = qs_card['init_balance']
        quantity = int(qs_card['quantity'])
        card_id = qs_card['id']
        if action == 'query':
            sheetid = request.POST.get('sheetid', '')
            count = request.POST.get('count', '')
            price = request.POST.get('price', '')
            card_list = data.getCodeBySheetID(sheetid, price, count)
            codes_correct = []
            codes_error = []
            codes_temp = []
            for card in card_list:
                if card['Mode'] == '9':
                    codes_temp.append(card['cardNo'].strip())
                else:
                    codes_error.append(card['cardNo'].strip())
            qs_codes =  GiftCardCode.objects.values('code').filter(wx_card_id=wx_card_id)
            qs_code_list = [qs_code['code'] for qs_code in qs_codes ]

            for code in codes_temp:
                if code in qs_code_list:
                    codes_error.append(code)
                else:
                    codes_correct.append(code)

            codes_correct_num = len(codes_correct)
            codes_error_num = len(codes_error)

            return render(request, 'giftcard/card_code_up.html', locals())
        elif action == 'upload':
            access_token = MyView().token
            codes = request.POST.getlist('codes[]')
            res = {}
            if len(codes) > 100:
                res['status'] = 5
                res['msg'] = 'Code上传数量大于100'
                return HttpResponse(json.dumps(res))
            data_post = {
                "card_id": wx_card_id,
                "code": codes
            }
            # 上传code
            res_upload = method.upLoadCardCode(access_token, wx_card_id, data_post)

            code_success = []
            code_fail = []
            if res_upload['status'] == 0:
                code_success = codes
            elif res_upload['status'] == 1:
                # code未全部上传成功，则查询上传成功的code
                code_success = res_upload['success_code']
                code_fail = res_upload['fail_code']
            elif res_upload['status'] == 2:
                # 上传code报错
                res['status'] = 5  # 全部失败
                res['msg'] = '上传Code微信过程报错'
                return HttpResponse(json.dumps(res))

            res['code_success'] = ','.join(code_success)
            res['code_success_num'] = len(code_success)
            res['code_fail'] = ','.join(code_fail)
            res['code_fail_num'] = len(code_fail)

            try:
                with transaction.atomic():
                    # 存储wx_card_id与code的对应关系
                    codes = code_success
                    mode_list = []
                    for code in codes:
                        item = GiftCardCode()
                        item.wx_card_id = wx_card_id
                        item.code = code
                        mode_list.append(item)
                    GiftCardCode.objects.bulk_create(mode_list)
                    # #更新guest中code的状态
                    # res_update1 = method.updateCardMode(codes,9,1)
                    # if res_update1['status'] != 0:
                    #     raise MyException('Code状态更新失败')

                    if res_upload['status'] == 0:
                        res['status'] = 0  # 全部成功
                    elif res_upload['status'] == 1:
                        res['status'] = 1  # 部分成功

            except Exception as e:
                LogWx.objects.create(type='5', errmsg='transaction roll back', errcode='', remark=e)
                if res_upload['status'] == 0:
                    res['status'] = 2  # 全部Code上传微信成功，线下处理失败
                elif res_upload['status'] == 1:
                    res['status'] = 3  # 部分Code上传微信成功，线下处理失败
                if hasattr(e, 'value'):
                    res['msg'] = e.value

            return HttpResponse(json.dumps(res))


class CardCodeOnLine(MyView):
    """
    查询线上卡实例下属code数量
    """

    def get(self, request, wx_card_id):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/code/getdepositcount?access_token={token}' \
            .format(token=access_token)
        data = {
            "card_id": wx_card_id,
        }
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        rep = requests.post(url, data=data)
        rep_data = json.loads(rep.text)
        return HttpResponse(json.dumps(rep_data))


class CardModifyStockView(MyView):
    def post(self, request):
        access_token = MyView().token
        wx_card_id = request.POST.get('wx_card_id', '')
        increase = request.POST.get('increase', 0)
        reduce = request.POST.get('reduce', 0)
        res_modify = method.modifyCardStock(access_token, wx_card_id, increase, reduce)

        return HttpResponse(json.dumps(res_modify))


class CheckCodeInfo(MyView):
    def get(self, request, card_id, code):
        access_token = MyView().token
        rep_data = giftcard.getCardCodeInfo(access_token,card_id,code)
        return HttpResponse(json.dumps(rep_data))


class ChangeBalanceView(MyView):
    def get(self, request, card_id, code, balance):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/card/generalcard/updateuser?access_token={token}' \
            .format(token=access_token)
        data = {
            "code": code,
            "card_id": card_id,
            "balance": float(balance) * 100
        }

        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        rep = requests.post(url, data=data, headers={'Connection': 'close'})
        rep_data = json.loads(rep.text)
        if rep_data['errcode'] != 0:
            return HttpResponse('ok')
        else:
            return HttpResponse(rep_data['errmsg'])


class CardUnavailableView(MyView):
    def get(self,request):
        res = method.createResult(-1, '', {})
        return render(request, 'giftcard/code_unavailable.html',locals())

    @transaction.atomic
    def post(self,request):
        trans_id = request.POST.get('trans_id','')
        qs_order = GiftOrder.objects.values('id').filter(trans_id=trans_id,refund='0')
        if qs_order:
            order = qs_order.first()
            order_id = order['id']
            qs_order_info = GiftOrderInfo.objects.values('card_id','code').filter(order_id=order_id).first()

            access_token = MyView().token
            rep_data = giftcard.codeUnavailable(access_token,qs_order_info['code'],qs_order_info['card_id'])
            if rep_data['errcode'] == 0:
                try:
                    with transaction.atomic():
                        qs_order.update(refund='3')
                        GiftCardCode.objects.filter(wx_card_id=qs_order_info['card_id'],code=qs_order_info['code'])\
                            .update(status='3')
                        res = method.createResult(0,'ok',{})
                except Exception as e:
                    res = method.createResult(3, e, {})
            else:
                res = method.createResult(2, rep_data['errmsg'],{})
        else:
            res = method.createResult(1, 'trans_id is not exist',{})

        return render(request, 'giftcard/code_unavailable.html', locals())

