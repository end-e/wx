# -*-  coding:utf-8 -*-
from api.models import LogWx

__author__ = ''
__date__ = '2017/6/20 8:53'
import json
import requests
import urllib.parse

from django.shortcuts import render
from django.views.generic.base import View

from admin.models import GiftTheme,GiftImg,GiftPage
from admin.utils.myClass import MyView,MyException
from admin.utils import method


class UploadPageView(MyView):
    def get(self, request, page_id):
        base_theme_list = GiftTheme.objects.values('title', 'id').filter(status='0')
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        if page_id == '0':
            # TODO 新建
            return render(request, 'giftcard/page_create.html', locals())

        else:
            # TODO 查询相关信息，供修改页面展示
            # page_id=sO898gip2rDKIDXgaMcqTXSy64LOxmDMrEGdoxmrGeA=
            # page_id=urllib.parse.quote(page_id)
            # page_id = 'sO898gip2rDKIDXgaMcqTXSy64LOxmDMrEGdoxmrGeA%3d'
            # page_id = urllib.parse.unquote(page_id)
            # access_token = MyView().token
            # url = 'https://api.weixin.qq.com/card/giftcard/page/get?access_token={access_token}' \
            #     .format(access_token=access_token)
            # data = {"page_id": page_id}
            # data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            #
            # response = requests.post(url, data=data)
            # res_data = json.loads(response.text)
            #
            # if res_data['errmsg'] == 'ok':
            #     page = res_data['page']
            # else:
            #     errcode = res_data['errcode']
            #     errmsg = res_data['errmsg']

            page = GiftPage.objects.values('title','banner_pic','categories','themes','wx_page_id')\
                .get(pk=page_id)
            if page['categories'] != '':
                category_list = page['categories'].split(',')
                page['category_list']=category_list
            if page['themes'] != '':
                theme_list = page['themes'].split(',')
                page['theme_list'] = theme_list
            return render(request, 'giftcard/page_create.html', locals())

    def post(self, request, page_id):
        access_token = MyView().token
        if page_id == '0':
            #TODO 新建货架
            url = "https://api.weixin.qq.com/card/giftcard/page/add?access_token={access_token}" \
                .format(access_token=access_token)
            #1、接收表单提交数据
            page_title = request.POST.get('page_title')
            banner_pic_url = request.POST.get('banner_pic_url')
            themes = request.POST.getlist('theme[]')
            theme_categories = request.POST.getlist('theme_category[]')
            categories = request.POST.getlist('category[]')

            #2、为本地存储整理数据
            theme_category_str = ''
            for i in range(0, len(themes)):
                theme_category_str += str(themes[i]) + ':' + str(theme_categories[i]) + ','
            theme_category_str = theme_category_str[0:len(theme_category_str) - 1]

            m_page = GiftPage.objects.create(
                title=page_title, banner_pic=banner_pic_url,
                categories=categories.join(','), themes=theme_category_str
            )

            # 3、微信数据上传
            # 3.1、category_list
            category_list = [{'title': category} for category in categories]
            # 3.2、theme_list
            theme_list = method.createThemeList(themes,theme_categories)
            # 3.3、data
            data = method.carePageData(page_title,banner_pic_url,theme_list,category_list)
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            # 3.4、post数据
            response = requests.post(url, data=data)
            # 3.5、接收respond
            res_data = json.loads(response.text)

            if res_data['errmsg'] == 'ok':
                wx_page_id = res_data['page_id']
                wx_page_id = urllib.parse.quote(wx_page_id)
                home_url = "https://mp.weixin.qq.com/bizmall/giftcard?action=homepage&page_id={page_id}#wechat_redirect" \
                    .format(page_id=wx_page_id)
                GiftPage.objects.filter(id=m_page.id).update(wx_page_id = wx_page_id,wx_page_url=home_url)

            else:
                errcode = res_data['errcode']
                errmsg = res_data['errmsg']

        else:
            #TODO 货架信息修改接口
            res = {}
            try:
                if not access_token:
                    raise MyException('access_token缺失')
                url = "https://api.weixin.qq.com/card/giftcard/page/update?access_token={access_token}" \
                    .format(access_token=access_token)

                wx_page_id = request.POST.get('wx_page_id')
                page_title = request.POST.get('page_title')
                banner_pic_url = request.POST.get('banner_pic_url')

                themes = request.POST.getlist('theme[]')
                theme_categories = request.POST.getlist('theme_category[]')
                theme_category_str = ''
                for i in range(0, len(themes) ):
                    theme_category_str += str(themes[i])+':'+str(theme_categories[i])+','
                theme_category_str = theme_category_str[0:len(theme_category_str)-1]

                categories = request.POST.getlist('category[]')
                #本地数据保存
                GiftPage.objects.filter(id=page_id).update(
                    title=page_title, banner_pic=banner_pic_url,
                    categories=','.join(categories), themes=theme_category_str
                )

                #微信数据上传
                # 1、category_list
                category_list = [{'title': category} for category in categories]
                # 2、theme_list
                theme_list = method.createThemeList(themes,theme_categories)
                # 3、data
                data = method.carePageData(page_title, banner_pic_url, theme_list, category_list)
                data['page']['page_id'] = wx_page_id
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')
                # 4、post数据
                rep = requests.post(url, data=data)
                # 5、接收respond
                rep_data = json.loads(rep.text)

                if rep_data['errmsg'] == 'ok':
                    res["status"] = 0
                else:
                    LogWx.objects.create(
                        type='4',
                        errmsg=rep_data['errmsg'],
                        errcode=rep_data['errcode']
                    )

            except Exception as e:
                msg =e
                res["status"] = 1
                if hasattr(e, 'value'):
                    msg = e.value
                    res['msg'] = msg
                LogWx.objects.create(
                    type='4',
                    errmsg=msg,
                    errcode='4'
                )

        return render(request, 'giftcard/page_create.html', locals())


class PageView(View):
    def get(self,request):
        page_list = GiftPage.objects.values('id','title','wx_page_id')
        return render(request,'giftcard/page_list.html',locals())
