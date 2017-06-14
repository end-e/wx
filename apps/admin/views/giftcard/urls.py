# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/14 10:26'
from django.conf.urls import url

from admin.views.giftcard import upload

urlpatterns = [
    url('upload/img',upload.UploadImgView,name='upload_img'),
]