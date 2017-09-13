# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:22'
import datetime,json

from django.core.cache import caches
from django.http import HttpResponse

from utils import db,consts
from api.models import  LogShop

def createOrderSn(objModel):
    today = datetime.datetime.today()
    begin = today.strftime('%Y-%m-%d') + ' 00:00:00'
    end = today.strftime('%Y-%m-%d') + ' 23:59:59'

    count = objModel.objects.filter(save_time__lte=end, save_time__gte=begin).count()
    sn = str(count + 1).zfill(4)
    sn = today.strftime('%Y%m%d') + sn

    return sn


def getGuest(card_no):
    conn = db.getMsSqlConnection(
        consts.DB_SERVER_22, consts.DB_PORT_22, consts.DB_USER_22,
        consts.DB_PASSWORD_22, consts.DB_DATABASE_22
    )
    sql = "select a.point,a.memberid from guest a,cardtype b " \
        "where a.CardType=b.cardtype and b.flag=0 and a.mode='1'and a.Point>0 and  cardno='{card_no}' " \
        "and CONVERT(char(10),a.EndDate,120)>=convert(char(10),GETDATE(),120) "\
        .format(card_no=card_no)
    cur = conn.cursor()
    cur.execute(sql)
    guest = cur.fetchone()
    if guest:
        return guest
    else:
        return None



def updateGuestPoint(member_id,card_no,total_pay,result_point):
    conn = db.getMsSqlConnection(
        consts.DB_SERVER_22, consts.DB_PORT_22, consts.DB_USER_22,
        consts.DB_PASSWORD_22, consts.DB_DATABASE_22, None
    )
    try:

        conn.autocommit(False)

        update_guest = "update Guest  set Point={result_point},LastUseDate=GETDATE(),LastShopID='K001' " \
                       "where CardNo='{CardNo}'".format(result_point=result_point,CardNo=card_no)
        cur = conn.cursor()
        cur.execute(update_guest)

        update_shop_guest = "update ShopGuest set Point=Point-{total_pay} where CardNo='{CardNo}' and Shopid='K001'"\
            .format(total_pay=total_pay,CardNo=card_no)
        cur.execute(update_shop_guest)
        if cur.rowcount==0:
            insert_shop_guest = "insert into shopGuset (ShopID,CardNo,Point) values ('K001','{CardNo}',{Point})"\
                .format(CardNo=card_no,Point=-float(total_pay))
            cur.execute(insert_shop_guest)

        today = datetime.datetime.today().date()
        sheet_id = 'K001'+datetime.datetime.strftime(today,'%Y%m%d')+'9999'
        insert_cardacc0 = "insert into cardacc0 " \
            "(cardNo,MemberID,ShopID,OccurDate,RecordDate,DirectFlag,Value,ResultValue,Point,ResultPoint,SheetID,SheetType,Note) " \
            "values ('{cardNo}','{MemberID}','K001',GETDATE(),GETDATE(),-1,0,0,{bm_point},{ResultPoint},'{sheetid}','880001','卡积分消减(宽广豆)') "\
            .format(cardNo=card_no,MemberID=member_id,bm_point=total_pay,ResultPoint=result_point,sheetid=sheet_id)
        cur.execute(insert_cardacc0)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return None


def getWxUser(request):
    token = request.META.get('HTTP_TOKEN', '')
    userInfo = caches['default'].get(token, '')

    return userInfo


def getWxUserOpenID(request):
    token = request.META.get('HTTP_TOKEN', '')
    userInfo = caches['default'].get(token, '')
    openid = ''
    if userInfo:
        openid = userInfo.get('openid','')

    return openid


def createLogShop(log):
    kwargs = {}
    kwargs.setdefault('errmsg',log['errmsg'])
    kwargs.setdefault('errcode',log['errcode'])
    if 'remark' in log:
        kwargs.setdefault('remark', log['remark'])
    LogShop.objects.create(**kwargs)


