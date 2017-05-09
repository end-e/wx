# -*- coding:utf-8 -*-
import datetime
import json

from django.shortcuts import render
from django.views.generic import View
from wechatpy import WeChatOAuth

from utils import db
from .models import WechatMembers
from .form import BoundForm


class MembersBoundView(View):
    def get(self, request):
        # 微信通过网页授权后返回的code
        code = request.GET.get('code', '')

        # 通过code获取网页授权access_token，这里的access_token不同于与调用接口的access_token不同
        res = WeChatOAuth.fetch_access_token(code)
        # 因为这里使用的授权作用域是snsapi_base，所以微信也返回了openid，snsapi_base网页授权流程到此为止
        # 如果使用的授权作用域是snsapi_userinfo，还需要继续使用网页授权access_token，详情见官网文档
        data = json.loads(res)
        openid = data['openid']
        access_token = data['access_token']

        return render(request, 'members_bound.html', {
            'openid': openid,
            'access_token': access_token,
        })

    def post(self, request):
        bound_form = BoundForm(request.POST)
        if bound_form.is_valid():
            # 会员姓名
            username = request.POST.get('username', '')
            # 手机号
            telphone = request.POST.get('telphone', '')
            # 身份证号
            idnumber = request.POST.get('idnumber', '')
            openid = request.POST.get('openid', '')
            access_token = request.POST.get('access_token', '')

            # 验证是否是实名制会员
            conn = db.getMysqlConn2()
            sql = "SELECT mem_number " \
                  "FROM uc_memcontent " \
                  "WHERE idc_name='{0}' AND idc_id='{1}' AND phonenumber='{2}'".format(username, idnumber, telphone)
            cur = conn.cursor()
            cur.execute(sql)
            member = cur.fetchall()
            if len(member) > 0:
                try:
                    WechatMembers.membernumber = member[0][0]
                    WechatMembers.openid = openid
                    WechatMembers.username = username
                    WechatMembers.telphone = telphone
                    WechatMembers.objects.save()
                except Exception as e:
                    return render(request, 'msg_warn.html', {'error': e})
                else:
                    return render(request, 'msg_success.html', {})
            else:
                return render(request, 'msg_warn.html', {'error': '请确认信息填写正确'})
