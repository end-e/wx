import random,hashlib

from django.core.cache import caches
from wechatpy import WeChatClient

from utils import db,consts


def createNonceStr(length = 16):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    str = ""
    for i in range(0,length):
        _index = random.randint(0, len(chars) - 1)
        str += chars[_index:_index+1]
    return str


def getShopName(id):
    """
    门店code==》门店名称
    :param id:
    :return:
    """
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




def get_ip(request):
    """
    获取ip
    :param request:
    :return:
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip




def md5(data):
    """
    md5加密
    :param data:
    :return:
    """
    md5 = hashlib.md5()
    if data:
        md5.update(data.encode(encoding = 'utf-8'))
    return md5.hexdigest()


def get_access_token(app_name,app_id,secret):
    client = WeChatClient(app_id, secret)
    response = client.fetch_access_token()
    token = response['access_token']
    key = 'wx_{app_name}_access_token'.format(app_name=app_name)
    caches['default'].set(key, token, 7200)

    return token
