# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/5/10 17:03'
from django.shortcuts import render
from django.core.cache import caches

from utils import db,consts

def getShopName(id):
    shopDict = caches['default'].get('base_shopDict','')
    if not shopDict:
        conn = db.getMysqlConnection(
            consts.DB_SERVER_18,
            consts.DB_PORT_18,
            consts.DB_USER_18,
            consts.DB_PASSWORD_18,
            consts.DB_DATABASE_18
        )
        sql = "SELECT Shopcode,Shopnm FROM bas_shop WHERE enable = 1"
        cur = conn.cursor()
        cur.execute(sql)
        shops = cur.fetchall()
        shopDict = {shop['Shopcode']:shop['Shopnm'].strip() for shop in shops}
        caches['default'].set('base_shopDict', shopDict,60*60*12)

    return shopDict[id]

