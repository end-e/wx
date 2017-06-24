# -*-  coding:utf-8 -*-
__author__ = 'chen'
__date__ = '2017/6/14 10:24'
import json
import os
import requests
import time
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View

from admin.models import GiftImg,GiftCategory,GiftTheme,GiftThemeItem,\
    GiftThemePicItem,GiftCard
from admin.utils.myClass import MyView


class ImgUploadAjaxView(MyView):
    """
    ajax提交
    """
    def post(self, request):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}' \
            .format(access_token=access_token)

        mypic = request.FILES.get('img', '')
        ext = os.path.splitext(mypic.name)[1]
        mypic.name = str(int(time.time())) + ext
        files = {'file': mypic}

        rep = requests.post(url, files=files)
        rep_data = json.loads(rep.text)

        res = {}
        if url in rep_data.keys():
            img_url = rep_data['url']
            res['status'] = 0
            res['img_url'] = img_url
        else:
            res['status'] = 1
            res['msg'] = rep_data['errmsg']


class ImgView(View):
    def get(self,request):
        img_list = GiftImg.objects.values('id','title','url').filter(status='0')
        return render(request, 'giftcard/img_list.html', locals())


class ImgUploadView(MyView):
    """
    form表单提交
    """
    def get(self, request):
        return render(request, 'giftcard/upload_img.html')

    def post(self, request):
        access_token = MyView().token
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}' \
            .format(access_token=access_token)

        title = request.POST.get('title','')
        mypic = request.FILES.get('img', '')
        ext = os.path.splitext(mypic.name)[1]
        mypic.name = str(int(time.time())) + ext
        files = {'file': mypic}

        rep = requests.post(url, files=files)
        rep_data = json.loads(rep.text)

        res = {}
        if 'url' in rep_data.keys():
            img_url = rep_data['url']
            try:
                GiftImg.objects.create(title = title,url=img_url)
                return redirect(reverse('admin:giftcard:imgs'))
            except:
                pass
        else:
            res['status'] = 1
            res['msg'] = rep_data['errmsg']


class CategoryView(View):
    def get(self,request):
        category_list = GiftCategory.objects.values('id','title').filter(status='0')
        return render(request,'giftcard/category_list.html',locals())


class CategoryEditView(View):
    def get(self,request,category_id):
        if category_id != '0':
            try:
                category = GiftCategory.objects.values('title','status').get(id=category_id)
            except:
                pass
        return render(request,'giftcard/category_edit.html',locals())
    def post(self,request,category_id):
        title = request.POST.get('title')
        status = request.POST.get('status')
        res = {}
        try:
            GiftCategory.objects.create(title=title,status=status)
            return redirect(reverse('admin:giftcard:categorys'))
        except Exception as e:
            res['status'] = 1
            return render(request, 'giftcard/category_edit.html', locals())


class ThemeView(View):
    def get(self,request):
        theme_list = GiftTheme.objects.values('id','title','theme_pic','create_time')\
            .filter(status='0')
        return render(request,'giftcard/theme_list.html',locals())


class ThemeEditView(View):
    def get(self,request,theme_id):
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        card_list = GiftCard.objects.values('title', 'wx_card_id').filter(status='2')
        if theme_id != '0':
            try:
                theme = GiftTheme.objects\
                    .values('id','title','theme_pic','title_color','sku_title_first','status')\
                    .get(id=theme_id)
                item_list = GiftThemeItem.objects.values('card_id','title').filter(theme_id=theme['id'])
                pic_item_list = GiftThemePicItem.objects.values('background_pic','msg')\
                    .filter(theme_id=theme['id'])
            except Exception as e:
                print(e)
                pass
        return render(request,'giftcard/theme_edit.html',locals())
    def post(self,request,theme_id):
        res = {}
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        card_list = GiftCard.objects.values('title', 'wx_card_id').filter(status='1')
        step_id = request.POST.get('step')
        if step_id == '1':
            title = request.POST.get('title')
            title_color = request.POST.get('title_color')
            theme_pic = request.POST.get('theme_pic')
            sku_title_first = request.POST.get('sku_title_first','0')
            status = request.POST.get('status')
            try:
                if theme_id == '0' :
                    th = GiftTheme.objects.create(
                        title=title,theme_pic=theme_pic,title_color=title_color,
                        status=status,sku_title_first=sku_title_first
                    )
                    th_id = th.id
                else:
                    GiftTheme \
                        .objects \
                        .filter(id=theme_id) \
                        .update(title=title, theme_pic=theme_pic, title_color=title_color,
                                status=status,sku_title_first=sku_title_first)
                res['status'] = 0
            except Exception as e:
                print(e)
                res['status'] = 1
        if step_id == '2':
            th_id = request.POST.get('th_id')
            card_ids = request.POST.getlist('item_card_id[]')
            card_titles = request.POST.getlist('item_card_title[]')
            try:
                themeItem_list = []
                for i in (0,len(card_ids)-1):
                    themeItem = GiftThemeItem()
                    themeItem.theme_id = th_id
                    themeItem.card_id = card_ids[i]
                    themeItem.title = card_titles[i]
                    themeItem_list.append(themeItem)
                GiftThemeItem.objects.bulk_create(themeItem_list)
                res['status'] = 0
            except Exception as e:
                print(e)
                res['status'] = 1
        if step_id == '3':
            th_id = request.POST.get('th_id')
            card_pics = request.POST.getlist('card_pic[]')
            card_msgs = request.POST.getlist('card_msg[]')
            try:
                themePicItem_list = []
                for i in (0, len(card_pics)):
                    themePicItem = GiftThemePicItem()
                    themePicItem.theme_id = th_id
                    themePicItem.background_pic = card_pics[i]
                    themePicItem.msg = card_msgs[i]
                    themePicItem_list.append(themePicItem)
                GiftThemePicItem.objects.bulk_create(themePicItem_list)
                res['status'] = 0
            except Exception as e:
                print(e)
                res['status'] = 1
        return render(request, 'giftcard/theme_edit.html', locals())



