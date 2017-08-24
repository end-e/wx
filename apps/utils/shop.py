# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:22'
import datetime

from utils import db
from admin.models import GiftBalanceChangeLog
from api.models import LogWx

def createOrderSn(objModel):
    today = datetime.datetime.today()
    begin = today.strftime('%Y-%m-%d') + ' 00:00:00'
    end = today.strftime('%Y-%m-%d') + ' 23:59:59'

    count = objModel.objects.filter(save_time__lte=end, save_time__gte=begin).count()
    sn = str(count + 1).zfill(4)
    sn = today.strftime('%Y%m%d') + sn

    return sn


def getGuestPoint(member_id):
    conn = db.getMsSqlConn()
    sql = "SELECT Point FROM guest as a,cardType as b WHERE cardNO='{cardNO}' AND b.flag='0'".format(cardNO=member_id)
    cur = conn.cursor()
    cur.execute(sql)
    guest = cur.fetchone()
    point = 0
    if guest:
        point = float(guest['Point'])
    return point


def updateGuestPoint(member_id,total_pay):
    conn = db.getMsSqlConn()
    cur = conn.cursor()
    res = True
    try:
        conn.autocommit(False)
        sql =  "UPDATE guest SET Point = Point-{total_pay} WHERE cardNO='{cardNO}'"\
            .format(cardNO=member_id,total_pay=total_pay)
        cur.execute(sql)
        if cur.rowcount == 1:
            conn.commit()
        else:
            res = False
    except Exception as e:
        print(e)
        conn.rollback()
        res = False

    return res