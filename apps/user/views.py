# -*- coding:utf-8 -*-
from urllib import parse

from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import IntegrityError
from django.http import HttpResponse
from wechatpy import WeChatOAuth

from utils import db
from .models import WechatMembers
from .form import BoundForm
from utils import consts


class MembersBoundView(View):
    def get(self, request):
        # 微信通过网页授权后返回的code
        code = request.GET.get('code', '')
        if not code:
            return redirect(
                u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/membersbound&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect')

        # 会员绑定页面 urlEncode，除0~9，a~Z外，全部转换成ascii形式
        redirect_uri = parse.quote('http://www.zisai.net/user/membersbound/')
        # 通过code获取网页授权access_token，这里的access_token不同于与调用接口的access_token不同
        oauth = WeChatOAuth(consts.APPID, consts.APPSECRET, redirect_uri)
        res = oauth.fetch_access_token(code)
        # 因为这里使用的授权作用域是snsapi_base，所以微信也返回了openid，snsapi_base网页授权流程到此为止
        # 如果使用的授权作用域是snsapi_userinfo，还需要继续使用网页授权access_token，详情见官网文档
        openid = res['openid']
        access_token = res['access_token']

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
            cur = conn.cursor()
            # 将身份证最后一位的x转换为大写
            if str(idnumber)[-1] == 'x':
                idnumber = str(idnumber).upper()
            sql = "SELECT mem_number FROM uc_memcontent WHERE idc_name='{0}' AND idc_id='{1}' AND phonenumber='{2}'".format(
                username, idnumber, telphone)
            cur.execute(sql)
            member = cur.fetchall()
            if member:
                membership = member[0]['mem_number']
                try:
                    wechat_member = WechatMembers()
                    wechat_member.membernumber = membership
                    wechat_member.openid = openid
                    wechat_member.username = username
                    wechat_member.telphone = telphone
                    wechat_member.save()
                except IntegrityError:
                    return render(request, 'msg_warn.html', {'error': u'此微信已绑定会员'})
                except Exception as e:
                    return render(request, 'msg_warn.html', {'error': e})
                else:
                    return render(request, 'msg_success.html', {})
            else:
                return render(request, 'msg_warn.html', {'error': u'请确认信息填写正确'})


class MembersImageView(View):
    def get(self, request):
        # 微信通过网页授权后返回的code
        code = request.GET.get('code', '')
        if not code:
            return redirect(
                u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/membersimage&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect')

        # 会员绑定页面 urlEncode，除0~9，a~Z外，全部转换成ascii形式
        redirect_uri = parse.quote('http://www.zisai.net/user/membersimage/')
        # 通过code获取网页授权access_token，这里的access_token不同于与调用接口的access_token不同
        oauth = WeChatOAuth(consts.APPID, consts.APPSECRET, redirect_uri)
        res = oauth.fetch_access_token(code)
        # 因为这里使用的授权作用域是snsapi_base，所以微信也返回了openid，snsapi_base网页授权流程到此为止
        # 如果使用的授权作用域是snsapi_userinfo，还需要继续使用网页授权access_token，详情见官网文档
        openid = res['openid']
        access_token = res['access_token']

        member_num=''
        member_info = WechatMembers.objects.values('membernumber').filter(openid=openid)

        if member_info is None:
            pass
        else:
            member_num = member_info[0][0]

        return render(request, 'members_image.html', {
            'openid': openid,
            'access_token': access_token,
            'member_num': member_num,
        })
