# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:36'
import datetime,json

from django.core.cache import caches
from django.db import transaction
from django.http import HttpResponse

from user.models import WechatMembers
from utils import db,method as mth
from admin.utils import method
from admin.models import GiftOrder, GiftOrderInfo, GiftCardCode, GiftBalanceChangeLog
from api.models import LogWx


def get_user_order():
    # TODO：查询ERP内的消费数据
    try:
        conn = db.getMsSqlConn()
        cur = conn.cursor()
        print('conn')
        if not cur:
            raise (NameError, "连接数据库失败")
        start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        last_purchserial = caches['default'].get('wx_ikg_tempmsg_last_purchserial', '')
        if last_purchserial:
            whereStr = "a.PurchSerial> '{last_purchserial}'".format(last_purchserial=last_purchserial)
        else:
            whereStr = "a.PurchDateTime> '{start}'".format(start=start)

        sql = "SELECT a.PurchSerial, a.PayMoney,a.CardNo,a.PurchDateTime,a.shopID,a.Point,a.HistoryPoint,a.ListNO,a.Branchno" \
              " FROM GuestPurch0 AS a with (nolock),guest AS b with (nolock),cardtype AS c with (nolock)" \
              " WHERE " + whereStr + " AND a.cardno=b.cardno AND  b.cardtype = c.cardtype AND  c.flag = 0" \
              " ORDER BY a.PurchSerial"

        cur.execute(sql)
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return orders
    except Exception as e:
        print(e)
        return []


def get_wechat_users(orders):
    users = [order['CardNo'].strip() for order in orders]
    wechat_users = WechatMembers.objects.values('openid', 'username', 'membernumber').filter(membernumber__in=users)

    return wechat_users


def getGuestPurch(start,prev_last_serial):
    if prev_last_serial:
        whereStr = "a.PurchSerial> '{last_serial}'".format(last_serial=prev_last_serial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    try:
        conn_226 = db.getMsSqlConn()
        sql_order = "SELECT a.detail, a.CardNo,a.PurchSerial" \
                    " FROM GuestPurch0 AS a with (nolock) ,guest AS b with (nolock)" \
                    " WHERE " + whereStr + " AND a.CardNo=b.CardNo AND b.cardtype = 12" \
                    " ORDER BY a.PurchSerial "
        cur_226 = conn_226.cursor()
        cur_226.execute(sql_order)
        orders = cur_226.fetchall()
    except Exception as e:
        orders = []
        method.createLog('2', '1201', e, 'guestPurch0 fail')

    return orders


def getGiftBalance():
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    balanceChangeLog = GiftBalanceChangeLog.objects.values('last_serial').first()
    prev_last_serial = ''
    if balanceChangeLog:
        prev_last_serial = balanceChangeLog['last_serial']
    orders = getGuestPurch(start,prev_last_serial)

    if len(orders)>0:
        update_serial = True
    else:
        update_serial = False

    log_list = LogWx.objects.values('id', 'remark', 'repeat_status') \
        .filter(type='2', errcode__in=['41001','40001', '40073', '-1', '45009','40056','1202'], repeat_status='0')
    for log in log_list:
        item = {}
        remark_list = log['remark'].split(',')
        for remark in remark_list:
            r = remark.split(':')
            item[r[0]] = r[1]
        item['id'] = log['id']
        item['repeat_status'] = log['repeat_status']
        orders.append(item)

    orders = sorted(orders, key=lambda order: int(order['PurchSerial']))
    this_last_serial = orders[-1]['PurchSerial']
    if update_serial:
        if prev_last_serial:
            now = datetime.datetime.now()
            GiftBalanceChangeLog.objects.filter(last_serial=prev_last_serial) \
                .update(last_serial=this_last_serial, create_time=now.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            GiftBalanceChangeLog.objects.create(last_serial=this_last_serial)
    if len(orders)>0:
        res = {'status':True,'orders':orders}
    else:
        res = {'status':False}
    return res


def local_save_gift_order(wx_orders,diff):
    for order in wx_orders:
        if order['order_id'] in diff:
            saveAndUpdateLocalData(order)


@transaction.atomic
def saveAndUpdateLocalData(order):
    try:
        with transaction.atomic():
            order_save = GiftOrder.objects.create(
                order_id=order['order_id'], trans_id=order['trans_id'],
                create_time=order['create_time'], pay_finish_time=order['pay_finish_time'],
                total_price=order['total_price'], open_id=order['open_id']
            )
            orderID = order_save.id
            info_list = []
            card_code_list = []
            code_list = []
            for card in order['card_list']:
                #order_info
                info = GiftOrderInfo()
                info.order_id = orderID
                info.card_id = card['card_id']
                info.price = card['price']
                info.code = card['code']
                info_list.append(info)

                #card_code
                qs_code = GiftCardCode.objects.filter(wx_card_id=card['card_id'],code=card['code'])
                if not qs_code:
                    card_code = GiftCardCode()
                    card_code.wx_card_id = card['card_id']
                    card_code.code = card['code']
                    card_code.status = '1'
                    card_code_list.append(card_code)
                else:
                    code_list.append(card['code'])

            GiftOrderInfo.objects.bulk_create(info_list)
            if len(card_code_list)>0:
                GiftCardCode.objects.bulk_create(card_code_list)
            GiftCardCode.objects.filter(code__in=code_list).update(status='1')
            # 更改guest状态
            method.updateCardMode(code_list, 9, 1)

    except Exception as e:
        method.createLog('6', '1101', e, order['order_id'])


def getCodeBySheetID(sheetid, price, count=100):
    num_new = 100 if int(count) > 100 else int(count)
    conn = db.getMsSqlConn()
    sql = "SELECT TOP {num} cardNo,Mode,New_amount FROM guest with (nolock) " \
          "WHERE cardType='12' AND sheetid='{sheetid}' AND New_amount={value} AND Detail ={value} " \
          "ORDER BY cardNo" \
        .format(sheetid=sheetid, value=price, num=num_new)

    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()

    return data


def getCardsBalance(code_list):
    codes = "'" + "','".join(code_list) + "'"
    conn = db.getMsSqlConn()
    sql = "SELECT cardNo,Detail,New_amount FROM Guest with (nolock) WHERE CardNo in ({codes})".format(codes=codes)

    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()

    return data


def getCouponInfo(request):
    coupon_type_id = request.POST.get('coupon_type_id','').strip()
    conn = db.getMsSqlConn22()
    sql = "SELECT StartDate,EndDate,PayValue,Value,CouponTypeName FROM MyShop_CouponType WHERE CouponTypeID='{id}'"\
        .format(id=coupon_type_id)
    with conn :
        cur = conn.cursor()
        cur.execute(sql)
        coupon = cur.fetchone()
        coupon['PayValue'] = float(coupon['PayValue']) if coupon['PayValue'] else 0
        coupon['Value'] = float(coupon['Value']) if coupon['Value'] else 0
        coupon['StartDate'] = datetime.datetime.strftime(coupon['StartDate'],'%Y-%m-%d')
        coupon['EndDate'] = datetime.datetime.strftime(coupon['EndDate'],'%Y-%m-%d')
        if coupon :
            res = mth.createResult('0','ok',{'coupon':coupon})
        else:
            res = mth.createResult('1','no data')

    return HttpResponse(json.dumps(res))

def insertCoupon(coupon):
    conn = db.getMsSqlConn22()
    cur = conn.cursor()
    # 插入临时MyShop_Coupon99
    sql = "Insert into MyShop_Coupon99" \
          "(CouponID,ShopID,CouponNO,CouponTypeID,StartDate,EndDate," \
          "CPWdFlag,CPwd,UseTime,MaxUseTime,Value," \
          "Discount,Flag,FromSheetType,FromSDate,FromListNO," \
          "FromPOSID,SerialID,ClearFlag) " \
          "Values({coupon},{shop},{sn},{type},GETdate(),{end},0,null ,0,1,{value},0,0,220,{create},null,{name},{batch},0)" \
        .format(coupon='%s', shop='%s', sn='%s', type='%s', end='%s', value='%s', create='%s', name='%s', batch='%s')

    params = []

    for item in list:
        param = (coupon[6], coupon[0], item['voucher'], type, coupon[3], coupon[4], coupon[2], coupon[7],
                 coupon[6])
        params.append(param)
    try:
        cur.executemany(sql, params)
        conn.commit()
    except:
        conn.rollback()

    cur.close()
    cursor = conn.cursor()
    # 读取99表调用存储过程插入正式表
    sql = "exec IF_MyShop_Coupon99 @CouponID='" + cardinfo[6] + "'"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return
