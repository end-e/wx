from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from django.http import HttpResponse

from io import BytesIO
import json

from admin.utils import method
from admin.models import User
from admin.forms import LoginForm

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request, 'sys/index.html')


class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        return render(request, 'sys/login.html',locals())
    def post(self,request):
        u_name = request.POST.get('username').strip()
        u_pwd = request.POST.get('password').strip()
        u_vocde = request.POST.get('vcode').strip()
        msg = {}
        if not u_name or not u_pwd:
            msg['status'] = 1
        elif u_vocde != request.session.get('vcode', ''):
            msg['status'] = 2
        else:
            user = User.objects.filter(name=u_name, status='0').first()
            if not user:
                msg['status'] = 3
            else:
                u_pwd = method.md5('ikg' + u_pwd)
                if user.pwd != u_pwd:
                    msg['status'] = 4
                else:
                    msg['status'] = 0
                    request.session['user'] = user
                    navData = method.getUserNav(user.role)
                    navList = method.createNavList(navData)
                    request.session['user'].user_nav = navList
        return HttpResponse(json.dumps(msg), content_type="application/json")


class CodeView(View):
    def get(self,request):
        # 将image信息保存到BytesIO流中
        buff = BytesIO()
        image = method.verifycode(request, 'vcode')
        image.save(buff, "png")
        return HttpResponse(buff.getvalue(), 'image/png')


#注销
class LogoutView(View):
    def get(self,request):
        try:
            del request.session["user"]
        except:
            print(">>>>>>>>logout")

        return HttpResponseRedirect('admin/login')


#密码重置
class ResetPwdView(View):
    def get(self,request):
        return render(request, 'sys/reset.html')
    def post(self,request):
        msg = {}
        user = request.session["user"]
        try:
            pwd_new = request.POST.get("pwd_new","").strip()
            pwd_confirm = request.POST.get("pwd_confirm","").strip()
            if pwd_new and pwd_confirm and pwd_new == pwd_confirm:
                pwd = method.md5('ikg'+pwd_new)
                User.objects.filter(id=user.id).update(password=pwd)
                msg["status"] = 0
            else:
                msg["status"] = 1
        except Exception as e:
            print(e)
        return render(request, 'sys/reset.html', locals())


