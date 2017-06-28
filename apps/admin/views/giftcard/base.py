# -*-  coding:utf-8 -*-
__author__ = 'chen'
__date__ = '2017/6/14 10:24'
import json,os,requests,time

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View

from admin.models import GiftImg,GiftCategory,GiftTheme,GiftThemeItem,GiftThemePicItem,GiftCard
from admin.utils.myClass import MyView
from admin.utils.paginator import MyPaginator

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

        return HttpResponse(json.dumps(res))


class ImgView(View):
    def get(self,request,page_id):
        img_list = GiftImg.objects.values('id','title','url','status','create_time').order_by('status','-create_time')
        page_id = int(page_id) if int(page_id) else 1
        paginator = MyPaginator(img_list,10)
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
                return redirect(reverse('admin:giftcard:imgs',kwargs={'page_id':1}))
            except Exception as e:
                print(e)
                pass
        else:
            res['status'] = 1
            res['msg'] = rep_data['errmsg']

        return render(request, 'giftcard/upload_img.html',locals())


class ImgStatusView(View):
    def get(self,request,img_id,status):
        update_num = GiftImg.objects.filter(id=img_id).update(status=status)
        res = {}
        if update_num:
            res['status'] = 0
        else:
            res['status'] = 1
        return HttpResponse(json.dumps(res))



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
    def get(self,request,theme_id,step_id):
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        card_list = GiftCard.objects.values('title', 'wx_card_id').filter(status='1')
        step_next = int(step_id)+1
        step_prev = int(step_id)-1
        th_id = theme_id
        if theme_id != '0':
            try:
                if step_id == '1':
                    theme = GiftTheme.objects\
                        .values('id','title','theme_pic','title_color','sku_title_first','status')\
                        .get(id=theme_id)
                elif step_id == '2':
                    item_list = GiftThemeItem.objects.values('id','wx_card_id','title').filter(theme_id=theme_id)
                elif step_id == '3':
                    pic_item_list = GiftThemePicItem.objects.values('id','background_pic','msg')\
                        .filter(theme_id=theme_id)
            except Exception as e:
                print(e)
                pass
        return render(request,'giftcard/theme_edit.html',locals())
    def post(self,request,theme_id,step_id):
        res = {}
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        card_list = GiftCard.objects.values('title', 'wx_card_id').filter(status='1')
        th_id = theme_id
        try:
            if step_id == '1':
                title = request.POST.get('title')
                title_color = request.POST.get('title_color')
                theme_pic = request.POST.get('theme_pic')
                sku_title_first = request.POST.get('sku_title_first','0')
                status = request.POST.get('status')
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

            if step_id == '2':
                th_id = request.POST.get('th_id')
                theme_ids = request.POST.getlist('theme_id[]')
                theme_card_ids = request.POST.getlist('theme_card_id[]')
                theme_card_titles = request.POST.getlist('theme_card_title[]')
                if len(theme_ids)==0:
                    themeItem_list = []
                    for i in range(0,len(theme_card_ids)):
                        themeItem = GiftThemeItem()
                        themeItem.theme_id = th_id
                        themeItem.wx_card_id = theme_card_ids[i]
                        themeItem.title = theme_card_titles[i]
                        themeItem_list.append(themeItem)
                    GiftThemeItem.objects.bulk_create(themeItem_list)

                else:
                    for i in range(0, len(theme_card_ids) ):
                        GiftThemeItem.objects.filter(id=theme_ids[i])\
                            .update(wx_card_id=theme_card_ids[i],title=theme_card_titles[i])

            if step_id == '3':
                th_id = request.POST.get('th_id')
                card_pic_ids = request.POST.getlist('card_pic_id[]')
                card_pics = request.POST.getlist('card_pic[]')
                card_msgs = request.POST.getlist('card_msg[]')
                if len(card_pic_ids)==0:
                    themePicItem_list = []
                    for i in range(0, len(card_pics)):
                        themePicItem = GiftThemePicItem()
                        themePicItem.theme_id = th_id
                        themePicItem.background_pic = card_pics[i]
                        themePicItem.msg = card_msgs[i]
                        themePicItem_list.append(themePicItem)
                    GiftThemePicItem.objects.bulk_create(themePicItem_list)
                else:
                    for i in range(0, len(card_pics)):
                        GiftThemePicItem.objects.filter(id=card_pic_ids[i])\
                            .update(background_pic = card_pics[i],msg = card_msgs[i])

            #跳转下一步
            kwargs = {'theme_id': theme_id, 'step_id': int(step_id)}
            return redirect(reverse('admin:giftcard:theme_edit', kwargs=kwargs))

        except Exception as e:
            print(e)
            res['status'] = 1
        return render(request, 'giftcard/theme_edit.html', locals())



