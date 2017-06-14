from django.db import connection
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont
import random,hashlib

from admin.utils import constants
from admin.models import RoleNav



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
          "from admin_rolenav as rn,admin_nav as n "\
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


#整理生成navTree
def createNavList(data):
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


#生成验证码
def  verifycode(request,key):
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
    if data.number < data.paginator.num_pages :
        num = data.paginator.next_page_num
    return num


def getPrePageNum(data):
    num = ''
    if data.number > 1:
        num = data.paginator.previous_page_num
    return num

