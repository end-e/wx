# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/24 18:06'
import random

def createNonceStr(length = 16):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    str = ""
    for i in range(0,length):
        _index = random.randint(0, len(chars) - 1)
        str += chars[_index:_index+1]
    return str