#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect


class LoginMiddleware(object):
    def process_request(self, request):
        path = request.path
        if path != '/admin/login/' and path != '/admin/vcode/' and path.find('admin')!=-1:
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/admin/login/')
        elif path == '/admin/login/':
            if request.session.get('user', None):
                return HttpResponseRedirect('/admin/')
            else:
                pass




