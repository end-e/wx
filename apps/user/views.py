# -*- coding:utf-8 -*-
from urllib import parse
import json,time

from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import IntegrityError
from django.http import HttpResponse
from django.core.cache import caches
from wechatpy import WeChatOAuth,WeChatClient

from utils import db
from .models import WechatMembers
from .form import BoundForm
from utils import consts
from user.utils import method


class MembersBoundView(View):
    def get(self, request):
        # 微信通过网页授权后返回的code
        code = request.GET.get('code', '')
        if not code:
            return redirect(
                u'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/membersbound&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
            )

        # 会员绑定页面 urlEncode，除0~9，a~Z外，全部转换成ascii形式
        redirect_uri = parse.quote('http://www.zisai.net/user/membersbound/')
        # 通过code获取网页授权access_token，这里的access_token不同于与调用接口的access_token不同
        oauth = WeChatOAuth(consts.APPID, consts.APPSECRET, redirect_uri)
        res = oauth.fetch_access_token(code)
        # 因为这里使用的授权作用域是snsapi_base，所以微信也返回了openid，snsapi_base网页授权流程到此为止
        # 如果使用的授权作用域是snsapi_userinfo，还需要继续使用网页授权access_token，详情见官网文档
        openid = res['openid']
        access_token = res['access_token']

        wx_access_token = caches['default'].get('wx_access_token', '')
        app_id = consts.APPID
        secret = consts.APPSECRET
        client = WeChatClient(app_id, secret, wx_access_token)
        jsapi = client.jsapi
        ticket = jsapi.get_jsapi_ticket()
        noncestr = method.createNonceStr()
        timestamp = int(time.time())
        url = "http://www.zisai.net/user/membersbound?code="+code+"&state=STATE"
        signature = jsapi.get_jsapi_signature(noncestr,ticket,timestamp,url)
        return render(request, 'members_bound.html',locals())

    def post(self, request):
        bound_form = BoundForm(request.POST)
        msg = {}
        if bound_form.is_valid():
            username = request.POST.get('username', '').strip()
            telphone = request.POST.get('telphone', '').strip()
            vcode = request.POST.get('vcode', '').strip()
            sms_code = caches['default'].get('sms_'+str(telphone))
            if not sms_code :
                #验证码不存在或失效
                msg['status'] = 4
                return HttpResponse(json.dumps(msg))
            if sms_code != int(vcode):
                msg['status'] = 5
                return HttpResponse(json.dumps(msg))

            idnumber = request.POST.get('idnumber', '')
            openid = request.POST.get('openid', '')
            access_token = request.POST.get('access_token', '')

            # 验证是否是实名制会员
            conn = db.getMysqlConn2()
            cur = conn.cursor()
            # 将身份证最后一位的x转换为大写
            if str(idnumber)[-1] == 'x':
                idnumber = str(idnumber).upper()
            sql = "SELECT mem_number,wx_tel FROM uc_memcontent " \
                  "WHERE idc_name='{0}' AND RIGHT(idc_id,6)='{1}'"\
                  .format(username, idnumber)
            cur.execute(sql)
            member = cur.fetchone()
            if member:
                if (member['wx_tel']!= telphone) or (not member['wx_tel']):
                    sql_update = "UPDATE uc_memcontent SET wx_tel='{tel}' " \
                                 "WHERE idc_name='{name}' AND RIGHT(idc_id,6)='{idc}'"\
                                 .format(name=username,tel= telphone,idc=idnumber)
                    cur.execute(sql_update)
                    conn.commit()
                    conn.close()
                    cur.close()
                membership = member['mem_number']
                try:
                    wechat_member = WechatMembers()
                    wechat_member.membernumber = membership
                    wechat_member.openid = openid
                    wechat_member.username = username
                    wechat_member.telphone = telphone
                    wechat_member.save()
                except IntegrityError:
                    #此微信已绑定会员
                    msg['status'] = 2
                    return HttpResponse(json.dumps(msg))
                except Exception as e:
                    #程序异常
                    msg['status'] = 3
                    return HttpResponse(json.dumps(msg))
                else:
                    msg['status'] = 0
                    return HttpResponse(json.dumps(msg))
            else:
                #用户不存在
                msg['status'] =1
                return HttpResponse(json.dumps(msg))
        else:
            msg['status'] = 1
            return HttpResponse(json.dumps(msg))


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

        member_num = ''
        member_info = WechatMembers.objects.values('membernumber').filter(openid=openid)
        # return HttpResponse(member_info)

        if not member_info:
            return render(request, 'msg_warn.html', {'error': u'此会员未实名制'})
        else:
            member_num = member_info[0]['membernumber']

        return render(request, 'members_image.html', {
            'openid': openid,
            'access_token': access_token,
            'member_num': member_num,
        })


class SuccessView(View):
    def get(self,request):
        return render(request,'msg_success.html')


