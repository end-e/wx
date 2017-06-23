# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/23 9:46'
from django import template

register = template.Library()

@register.filter('range')
def to_list(value):
    return range(1, int(value)+1)

@register.filter('int')
def to_int(val):
    return int(val)