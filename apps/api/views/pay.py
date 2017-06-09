# -*-  coding:utf-8 -*-
__author__ = ''
__date__ = '2017/6/6 9:02'
import hashlib
from urllib import parse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils import consts, wxPay


# @csrf_exempt
# @signature
def getPay(req):
    openid = req.GET.get('openId','')
    order_sn = req.GET.get('orderSn','')
    total_fee = req.GET.get('totalFee','')

    body = 'test'
    trade_type = 'JSAPI'
    # spbill_create_ip = method.getIP()

    # url = r'https://api.mch.weixin.qq.com/pay/unifiedorder'
    arr = {
        'out_trade_no': 'S201606080001',
        'body': body,
        'total_fee': '1',
        'trade_type': trade_type,
        'openid': 'oDZT50EikQkzMTZ28DzHx_eD4bVg'
    }
    unifiedOrder = wxPay.UnifiedOrder_pub()
    unifiedOrder.parameters= arr
    prepay_id = unifiedOrder.getPrepayId()


    # headers = {'Content-Type': 'text/xml', 'Connection': 'Keep-Alive'}
    # data = """
    # <xml>
    #     <appid>{appid}</appid>
    #     <device_info>{device_info}</device_info>
    #     <body>{body}</body>
    #     <mch_id>{mch_id}</mch_id>
    #     <nonce_str>{nonce_str}</nonce_str>
    #     <notify_url>{notify_url}</notify_url>
    #     <openid>{openid}</openid>
    #     <out_trade_no>{out_trade_no}</out_trade_no>
    #     <spbill_create_ip>{spbill_create_ip}</spbill_create_ip>
    #     <total_fee>{total_fee}</total_fee>
    #     <trade_type>{trade_type}</trade_type>
    #     <sign>{sign}</sign>
    # </xml>
    # """.format(appid=appid,device_info=device_info,body=body,mch_id=mch_id,nonce_str=nonce_str,
    #            notify_url=notify_url,out_trade_no=order_sn,total_fee=total_fee,
    #            trade_type=trade_type,spbill_create_ip=spbill_create_ip,sign=sign,openid=openid)
    #
    # resp = request.Request(url=url,headers=headers,data=data.encode('utf-8'))
    # page = request.urlopen(resp).read()
    # page = page.decode('utf-8')
    # page = xmlToArray(page)

    # res = {}
    # data = {}
    # data['timeStamp'] = timeStamp
    # data['nonceStr'] = nonceStr
    # res['data'] = data

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
    return_xml = ''
    if return_code == 'SUCCESS':
        try:
            openid = xml_recv.find("openid").text
            out_trade_no = xml_recv.find("out_trade_no").text
            #TODO 这里可以做成功之后的操作

            return_xml = '''
                <xml>
                    <return_code><![CDATA[SUCCESS]]></return_code>
                    <return_msg><![CDATA[OK]]></return_msg>
                </xml>'''
        except Exception as e:
            return_xml = '''
                <xml>
                    <return_code><![CDATA[FAIL]]></return_code>
                    <return_msg><![CDATA[参数格式校验错误]]></return_msg>
                </xml>'''
    else:
        return_xml = '''
                <xml>
                    <return_code><![CDATA[FAIL]]></return_code>
                    <return_msg><![CDATA[参数格式校验错误]]></return_msg>
                </xml>'''
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

import xml.etree.ElementTree as ET
def xmlToArray(xml):
    """将xml转为array"""
    array_data = {}
    root = ET.fromstring(xml)
    for child in root:
        value = child.text
        array_data[child.tag] = value
    return array_data