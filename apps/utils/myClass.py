# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/15 10:06'

class MyException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



