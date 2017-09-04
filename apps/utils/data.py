# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/8/24 14:36'
import datetime

from django.core.cache import caches
from django.db import transaction

from user.models import WechatMembers
from utils import db
from admin.models import GiftOrder, GiftOrderInfo, GiftCardCode, GiftBalanceChangeLog
from api.models import LogWx

def get_user_order():
    # TODO：查询ERP内的消费数据
    conn = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    last_purchserial = caches['default'].get('wx_ikg_tempmsg_last_purchserial', '')
    if last_purchserial:
        whereStr = "a.PurchSerial> '{last_purchserial}'".format(last_purchserial=last_purchserial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    sql = "SELECT a.PurchSerial, a.PayMoney,a.CardNo,a.PurchDateTime,a.shopID,a.Point,a.HistoryPoint,a.ListNO,a.Branchno " \
          "FROM GuestPurch0 AS a,guest AS b,cardtype AS c " \
          "WHERE " + whereStr + " AND a.cardno=b.cardno AND  b.cardtype = c.cardtype AND  c.flag = 0 " \
                                "ORDER BY a.PurchSerial"

    cur = conn.cursor()
    cur.execute(sql)
    orders = cur.fetchall()

    return orders


def get_wechat_users(orders):
    users = [order['CardNo'].strip() for order in orders]
    wechat_users = WechatMembers.objects.values('openid', 'username', 'membernumber').filter(membernumber__in=users)

    return wechat_users


def getGiftBalance():
    conn_226 = db.getMsSqlConn()
    start = datetime.datetime.now() + datetime.timedelta(minutes=-1)
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    balanceChangeLog = GiftBalanceChangeLog.objects.values('last_serial').first()
    prev_last_serial = ''
    if balanceChangeLog:
        prev_last_serial = balanceChangeLog['last_serial']
        whereStr = "a.PurchSerial> '{last_serial}'".format(last_serial=prev_last_serial)
    else:
        whereStr = "a.PurchDateTime> '{start}'".format(start=start)

    sql_order = "SELECT a.detail, a.CardNo,a.PurchSerial FROM GuestPurch0 AS a,guest AS b " \
                "WHERE " + whereStr + " AND a.CardNo=b.CardNo AND b.cardtype = 12 ORDER BY a.PurchSerial "


    cur_226 = conn_226.cursor()
    cur_226.execute(sql_order)
    orders = cur_226.fetchall()

    cardNo_list = [int(order['CardNo']) for order in orders]

    log_list = LogWx.objects.values('id','remark','repeat_status')\
        .filter(type='2',errcode__in=['40001','40073','-1'],repeat_status='0')

    for log in log_list:
        item = {}
        remark_list = log['remark'].split(',')
        for remark in remark_list:
            r = remark.split(':')
            item[r[0]] = r[1]
        if int(item['CardNo']) not in cardNo_list:
            item['id'] = log['id']
            item['repeat_status'] = log['repeat_status']
            orders.append(item)

    orders = sorted(orders,key= lambda order:int(order['PurchSerial']))

    return prev_last_serial,orders


def local_save_gift_order(wx_orders):
    for order in wx_orders:
        order_qs = GiftOrder.objects.filter(order_id=order['order_id'])
        if not order_qs:
            try:
                with transaction.atomic():
                    order_save = GiftOrder.objects.create(
                        order_id=order['order_id'], trans_id=order['trans_id'],
                        create_time=order['create_time'], pay_finish_time=order['pay_finish_time'],
                        total_price=order['total_price'], open_id=order['open_id']
                    )
                    orderID = order_save.id
                    info_list = []
                    code_list = []
                    for card in order['card_list']:
                        code_list.append(card['code'])
                        info = GiftOrderInfo()
                        info.order_id = orderID
                        info.card_id = card['card_id']
                        info.price = card['price']
                        info.code = card['code']
                        info_list.append(info)
                    GiftOrderInfo.objects.bulk_create(info_list)
                    GiftCardCode.objects.filter(code__in=code_list).update(status='1')
            except Exception as e:
                print(e)
                LogWx.objects.create(
                    type='6',
                    errmsg=e,
                    errcode='6',
                    remark='wx_order_id:{order}'.format(order=order['order_id'])
                )


def getCodeBySheetID(sheetid,price,count=100):
    num_new = 100 if int(count) > 100 else int(count)
    conn = db.getMsSqlConn()
    sql = "SELECT TOP {num} cardNo,Mode,New_amount FROM guest " \
          "WHERE cardType='12' AND sheetid='{sheetid}' AND New_amount={value} " \
          "ORDER BY cardNo" \
        .format(sheetid=sheetid, value=price, num=num_new)

    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()

    return data

