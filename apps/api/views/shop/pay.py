# -*-  coding:utf-8 -*-
from django.db import transaction

__author__ = ''
__date__ = '2017/6/6 9:02'
import hashlib
import xml.etree.ElementTree as ET
from urllib import parse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from utils import consts, wxPay,shop
from admin.models import ShopKgMoneyOrder, ShopUser
from api.models import LogWx

# @signature
def getPay(req):
    openid = req.GET.get('openId','')
    order_sn = req.GET.get('orderSn','')
    total_fee = req.GET.get('totalFee','')

    # url = r'https://api.mch.weixin.qq.com/pay/unifiedorder'
    arr = {
        'out_trade_no': order_sn,
        'body': 'pay',
        'total_fee': float(total_fee)*100,
        'trade_type': 'JSAPI',
        'openid': openid
    }
    unifiedOrder = wxPay.UnifiedOrder_pub()
    unifiedOrder.parameters= arr
    prepay_id = unifiedOrder.getPrepayId()

    return HttpResponse(prepay_id)

@csrf_exempt
def payNotify(request):
    recv_xml = request.body
    xml_recv = ET.fromstring(recv_xml)
    # {
    # "nonce_str": "Df6zRXdxb3Dt2BJCnbrsPdrdGkZfdDBG",
    # "out_trade_no": "S201606090001",
    # "return_code": "SUCCESS",
    # "openid": "oDZT50EikQkzMTZ28DzHx_eD4bVg",
    # "fee_type": "CNY",
    # "mch_id": "1410031002",
    # "total_fee": "1",
    # "cash_fee": "1",
    # "is_subscribe": "N",
    # "sign": "177468F545B0C0CA4176C4ED78EA2CDA",
    # "transaction_id": "4006862001201706094923521169",
    # "result_code": "SUCCESS",
    # "appid": "wxd5fbbceb077f7635",
    # "bank_type": "CFT",
    # "trade_type": "JSAPI",
    # "time_end": "20170609093241"
    # }
    return_code = xml_recv.find("return_code").text
    out_trade_no = xml_recv.find("out_trade_no").text
    openid = xml_recv.find("openid").text
    total_fee = xml_recv.find("total_fee").text
    remark = "sn:{sn},openid:{openid},total_fee:{total_fee}".format(sn=out_trade_no, openid=openid,total_fee=total_fee)
    flag = True
    if return_code == 'SUCCESS':
        try:
            with transaction.atomic():
                qs_order = ShopKgMoneyOrder.objects.filter(sn=out_trade_no)
                order = qs_order.values('count').first()
                count = int(order['count'])
                #更新用户宽豆数量
                ShopUser.objects.filter(openid=openid).update(kg_money=F('kg_money') + count)
                #更新订单状态
                qs_order.update(status='9')

                shop.createLogShop({"errcode":21399,"errmsg":"ok","remark":remark})
        except Exception as e:
            print(e)
            flag = False
            shop.createLogShop({"errcode": 21302, "errmsg": "wx pay success, local update fail", "remark": remark})
    else:
        flag = False
        remark = "sn:{sn},type:1".format(sn=out_trade_no)
        shop.createLogShop({"errcode": 21301, "errmsg": "wx pay fail", "remark": remark})

    if flag:
        return_xml = '''
        <xml>
            <return_code><![CDATA[SUCCESS]]></return_code>
            <return_msg><![CDATA[OK]]></return_msg>
        </xml>
        '''
    else:
        return_xml = '''
        <xml>
            <return_code><![CDATA[FAIL]]></return_code>
            <return_msg><![CDATA[参数格式校验错误]]></return_msg>
        </xml>
        '''
    return HttpResponse(return_xml)


def paysignjsapi(appid, attach, body, mch_id, nonce_str, notify_url, openid, out_trade_no, total_fee, trade_type):
    ret = {
        'appid': appid,
        'attach': attach,
        'body': body,
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'notify_url': notify_url,
        'openid': openid,
        'out_trade_no': out_trade_no,
        'total_fee': total_fee,
        'trade_type': trade_type
    }
    getSign(ret)

    return str


def formatBizQueryParaMap( paraMap, urlencode):
    """格式化参数，签名过程需要使用"""
    slist = sorted(paraMap)
    buff = []
    for k in slist:
        v = parse.quote(paraMap[k]) if urlencode else paraMap[k]
        buff.append("{0}={1}".format(k, v))

    return "&".join(buff)


def getSign(obj):
    """生成签名"""
    # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
    String = formatBizQueryParaMap(obj, False)
    # 签名步骤二：在string后加入KEY
    String = "{0}&key={1}".format(String, consts.WX_APP_KEY)
    # 签名步骤三：MD5加密
    String = hashlib.md5(String.encode(encoding='utf-8')).hexdigest()
    # 签名步骤四：所有字符转为大写
    result_ = String.upper()
    return result_


def xmlToArray(xml):
    """将xml转为array"""
    array_data = {}
    root = ET.fromstring(xml)
    for child in root:
        value = child.text
        array_data[child.tag] = value
    return array_data