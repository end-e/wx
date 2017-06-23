from django.db import connection
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont
import random, hashlib, time

from admin.utils import constants
from admin.models import RoleNav, GiftTheme, GiftThemeItem, GiftThemePicItem


def md5(data):
    md5 = hashlib.md5()
    if str:
        md5.update(data.encode(encoding='utf-8'))
    return md5.hexdigest()


def getTimeStamp(str):
    time.strptime(str, '%Y-%m-%d %H:%M:%S')
    return time.mktime(time.strptime(str, '%Y-%m-%d %H:%M:%S'))


def getUserNav(role_id=None):
    """
    根据用户role，获取navList
    :param role_id:
    :return:
    """

    # kwargs = {}
    # kwargs.setdefault('nav__status','0')
    # if role_id:
    #     role_id = role_id.split(',')
    #     kwargs.setdefault('role_id__in',role_id)
    #
    # plist = RoleNav.objects.values('nav_id','nav__name','nav__parent','nav__url','nav__icon','nav__sort')\
    #     .filter(**kwargs).order_by('nav__sort')

    sql = "select DISTINCT rn.role_id,rn.nav_id,n.name,n.parent,n.url,n.sort,n.icon " \
          "from admin_rolenav as rn,admin_nav as n " \
          "where rn.nav_id=n.id and n.status=0 "
    if role_id:
        role_id = str(role_id)
        sql += "and rn.role_id in (" + role_id + ") "

    sql += "order by n.sort "

    cursor = connection.cursor()
    cursor.execute(sql)
    plist = cursor.fetchall()
    rslist = []
    if plist:
        for p in plist:
            item = []
            item.append(("role", p[0]))
            item.append(("id", p[1]))
            item.append(("name", p[2]))
            item.append(("parent", p[3]))
            item.append(("url", p[4]))
            item.append(("sort", p[5]))
            item.append(("icon", p[6]))
            rslist.append(dict(item))

    return rslist


def createNavList(data):
    """
    拼接菜单列表数据
    :param data:
    :return:
    """
    m1list = sorted(data, key=lambda pur: pur["id"])
    menu_dict = {}
    if m1list:
        for p in m1list:
            if p["parent"] == '-1':
                p.setdefault("sub", [])
                menu_dict.setdefault("nav_" + str(p["id"]), p)
            else:
                pid = str(p["parent"])
                if "nav_" + pid in menu_dict and "sub" in menu_dict["nav_" + pid]:
                    menu_dict["nav_" + pid]["sub"].append(p)
    menu_list = [item for item in menu_dict.values()]

    menu_list = sorted(menu_list, key=lambda menu: menu["sort"])
    for item in menu_list:
        temp = sorted(item['sub'], key=lambda obj: obj["sort"])
        item['sub'] = temp
    return menu_list


def verifycode(request, key):
    # 随机颜色1:
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 240 x 60:
    width = 60 * 4
    height = 80
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    root = settings.BASE_DIR + constants.FONT_ARIAL
    font = ImageFont.truetype(root, 80)  # 36 - 字体大小，数值大字体大
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    # 输出文字:
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             # 'a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
             # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
             ]
    y = [y for y in [random.randint(x - x, len(chars) - 1) for x in range(4)]]
    charlist = [chars[i] for i in y]

    rcode = ''.join(map(str, charlist))

    for t in range(len(charlist)):
        draw.text((60 * t + 10, 3), charlist[t], font=font, fill=rndColor2())

    # 将验证码转换成小写的，并保存到session中
    request.session[key] = rcode

    return image


def getNextPageNum(data):
    num = ''
    if data.number < data.paginator.num_pages:
        num = data.paginator.next_page_num
    return num


def getNextPageNum2(current,total):
    current = int(current)
    num = 0
    if current < total:
        num = current+1
    return num


def getPrePageNum(data):
    num = ''
    if data.number > 1:
        num = data.paginator.previous_page_num
    return num


def getPrePageNum2(current):
    current = int(current)
    num = ''
    if current > 0:
        num = current-1
    return num


def createThemeList(themes,theme_categories):
    """
    礼品卡-货架-拼接theme_list
    :param themes: theme_id列表
    :return:
    """
    theme_list = []
    for i in (0,len(themes)-1):
        # theme
        t = GiftTheme.objects.values('id', 'title', 'theme_pic', 'title_color', 'sku_title_first').get(id=themes[i])

        d = {
            "theme_pic_url": t['theme_pic'],  # 主题的封面图片
            "title": t['title'],  # 主题名称
            "title_color": t['title_color'],  # 主题title的颜色
            "show_sku_title_first": bool(int(t['sku_title_first'])),  # 该主题购买页是否突出商品名显示
            "category_index": theme_categories[i] # 主题标号，对应category_list内的title字段
        }
        # item_list
        items = GiftThemeItem.objects.values('card_id', 'title').filter(theme_id=t['id'])
        item_list = []
        for item in items:
            i = {
                "card_id": item['card_id'],  # 待上架的card_id
                "title": item['title']  # 商品名，不填写默认为卡名称
            }
            item_list.append(i)
        d['item_list'] = item_list
        # pic_item_list
        pic_items = GiftThemePicItem.objects.values('background_pic', 'msg').filter(theme_id=t['id'])
        pic_item_list = []
        for pic_item in pic_items:
            p = {
                "background_pic_url": pic_item['background_pic'],  # 待上架的card_id
                "default_gifting_msg": pic_item['msg']  # 商品名，不填写默认为卡名称
            }
            pic_item_list.append(p)
        d['pic_item_list'] = pic_item_list

        theme_list.append(d)

    return theme_list


def carePageData(page_title, banner_pic_url, theme_list, category_list):
    """
    拼接货架页面信息
    :param page_title: 页面标题
    :param banner_pic_url: banner_pic背景图
    :param theme_list: 主题列表
    :param category_list: 分类列表
    :return:
    """
    data = {
        "page": {
            "page_title": page_title,  # 礼品卡货架名称
            "banner_pic_url": banner_pic_url,  # 礼品卡货架主题页顶部banner图片
            "theme_list": theme_list,
            "category_list": category_list,
            "address": "宽广集团各超市门店均可使用",
            "service_phone": "400 111 0314",
            "biz_description": "退款指引",
            "cell_1": {
                "title": "申请发票",
                "url": "https://open.weixin.qq.com"
            },
            "cell_2": {
                "title": "申请退款",
                "url": "https://mp.weixin.qq.com"
            }
        }
    }

    return data


def createCardData(form):
    """
    拼接新建实例，所需的数据
    :param form: 创建卡实例表单
    :return:
    """
    background_pic = form.cleaned_data['background_pic']
    logo = form.cleaned_data['logo']
    init_balance = form.cleaned_data['init_balance']
    title = form.cleaned_data['title']
    price = form.cleaned_data['price']
    max_give = form.cleaned_data['max_give']
    brand_name = form.cleaned_data['brand_name']
    description = form.cleaned_data['description']
    notice = form.cleaned_data['notice']
    quantity = form.cleaned_data['quantity']

    data = {
        "card": {
            "card_type": "GENERAL_CARD",
            "general_card": {
                "sub_card_type": "GIFT_CARD",
                "background_pic_url": background_pic,
                "base_info": {
                    "giftcard_info": {
                        "price": int(price) * 100
                    },
                    "logo_url": logo + "?wx_fmt=gif",
                    "max_give_friend_times": int(max_give),
                    "code_type": "CODE_TYPE_QRCODE",
                    "brand_name": brand_name,
                    "title": title,
                    "color": "Color020",
                    "notice": notice,
                    "service_phone": "400 111 0314",
                    "description": description,
                    "date_info": {
                        "type": "DATE_TYPE_PERMANENT"
                    },
                    "sku": {
                        "quantity": int(quantity)
                    },
                    "use_all_locations": False,
                    # "location_id_list": [
                    #     213059884
                    # ],
                    "get_limit": 0,
                    "use_custom_code": True,
                    "get_custom_code_mode": "GET_CUSTOM_CODE_MODE_DEPOSIT",
                    "can_give_friend": True,
                    # "center_title": "立即使用",
                    # "center_sub_title": "按钮下方的wording",
                    # "center_url": "www.qq.com",
                    # "custom_url_name": "新品推荐",
                    # "custom_url": "https://www.starbucks.com.cn/",
                    # "need_push_on_view": True
                },
                "supply_bonus": False,
                "supply_balance": True,
                "prerogative": "礼品卡享受更多优惠",
                "auto_activate": True,
                "init_balance": int(init_balance),
                # "custom_field1": {
                #     "name": "优惠券",
                #     "url": "http://mp.weixin.qq.com/s?__biz=MjM5Mzc0OTEwMA==&mid=402699549&idx=1&sn=1fe0eb3fb0041e3f10b755c5470c7db3#rd"
                # },
                # "custom_field2": {
                #     "name": "兑换券",
                #     "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx3be6367203f983ac&redirect_uri=https%3A%2F%2Fmp.weixin.qq.com%2Fbizmall%2Fcardlandingpage%3Fbiz%3DMjM5Mzc0OTEwMA%3D%3D%26page_id%3D41%26scene%3D1&response_type=code&scope=snsapi_base#wechat_redirect"
                # }
            }
        }
    }

    return data


def createCardEditData(form):
    """
    拼接修改卡实例，所需的数据
    :param form:
    :return:
    """
    qs_wx_card_id = form.cleaned_data['wx_card_id']
    logo = form.cleaned_data['logo']
    description = form.cleaned_data['description']
    notice = form.cleaned_data['notice']
    data = {
        "card_id": qs_wx_card_id,
        "general_card": {
            "base_info": {
                "logo_url": logo + "?wx_fmt=gif",
                "notice": notice,
                "description": description,
                "service_phone": "400 111 0314",
                "color": "Color020",
                "code_type": "CODE_TYPE_QRCODE",
                "date_info": {
                    "type": "DATE_TYPE_PERMANENT"
                },
                "get_limit": 0,
                "can_give_friend": True
            }
        }
    }

    return data
