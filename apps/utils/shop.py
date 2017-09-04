# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:22'
import datetime

from utils import db
from django.core.cache import caches

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

from utils import consts
def updateGuestPoint(member_id,total_pay):
    conn = db.getMsSqlConnection(
        consts.DB_SERVER_226,consts.DB_PORT_226,consts.DB_USER_226,
        consts.DB_PASSWORD_226,consts.DB_DATABASE_226,None
    )
    conn.autocommit(False)
    sql = "declare @retcode int " \
          "declare @retmsg varchar(255) " \
          "declare @l_point dec(8,2) " \
          "exec WR_Pointcut '{member_id}',{point},@retcode output,@retmsg output,@l_point output " \
          "select @retcode,@retmsg,@l_point"\
        .format(member_id=member_id,point=total_pay)
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchone()
    conn.commit()

    return res


def getWxUser(request):
    token = request.META.get('HTTP_TOKEN', '')
    userInfo = caches['default'].get(token, '')

    return userInfo

def getWxUserOpenID(request):
    token = request.META.get('HTTP_TOKEN', '')
    userInfo = caches['default'].get(token, '')
    openid = userInfo.get('openid','')

    return openid


