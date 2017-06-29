# -*-  coding:utf-8 -*-
__author__ = 'chen'
__date__ = '2017/6/14 10:24'
import json,os,requests,time

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View

from admin.models import GiftImg,GiftTheme,GiftThemeItem,GiftThemePicItem,GiftCard
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


class ThemeView(View):
    def get(self,request):
        theme_list = GiftTheme.objects.values('id','title','theme_pic','create_time')\
            .filter(status='0')
        return render(request,'giftcard/theme_list.html',locals())


class ThemeEditView(View):
    def get(self,request,theme_id,step_id):
        pic_list = GiftImg.objects.values('title', 'url').filter(status='0')
        card_list = GiftCard.objects.values('title', 'wx_card_id').filter(status='2')
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
                item_ids = request.POST.getlist('item_id[]')
                item_card_ids = request.POST.getlist('item_card_id[]')
                item_card_titles = request.POST.getlist('item_card_title[]')

                for i in range(0,len(item_card_ids)):
                    item_id = item_ids[i]
                    if item_id :
                        GiftThemeItem.objects.filter(id=item_id) \
                            .update(wx_card_id=item_card_ids[i], title=item_card_titles[i])
                    else:
                        GiftThemeItem.objects.create(
                            theme_id=th_id,wx_card_id = item_card_ids[i],title = item_card_titles[i]
                        )
            if step_id == '3':
                th_id = request.POST.get('th_id')
                pic_item_ids = request.POST.getlist('pic_item_id[]')
                pic_item_pics = request.POST.getlist('pic_item_pic[]')
                pic_item_msgs = request.POST.getlist('pic_item_msg[]')
                for i in range(0, len(pic_item_pics)):
                    pic_item_id = pic_item_ids[i]
                    if pic_item_id :
                        GiftThemePicItem.objects.filter(id=pic_item_id) \
                            .update(background_pic=pic_item_pics[i], msg=pic_item_msgs[i])
                    else:
                        GiftThemePicItem.objects.create(
                            theme_id=th_id,background_pic = pic_item_pics[i],msg = pic_item_msgs[i]
                        )
            #跳转下一步
            kwargs = {'theme_id': theme_id, 'step_id': int(step_id)}
            return redirect(reverse('admin:giftcard:theme_edit', kwargs=kwargs))
        except Exception as e:
            print(e)
            res['status'] = 1
        return render(request, 'giftcard/theme_edit.html', locals())



