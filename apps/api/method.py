# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/1 8:13'
import hashlib


def md5(data):
    md5 = hashlib.md5()
    if data:
        md5.update(data.encode(encoding = 'utf-8'))
    return md5.hexdigest()

