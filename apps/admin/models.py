from django.db import models
from datetime import datetime
# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=45)
    status = models.CharField(max_length=1, verbose_name=u'状态',default='0')

    class Meta:
        verbose_name = u'用户角色'
        verbose_name_plural = verbose_name


class Nav(models.Model):
    name = models.CharField(max_length=45)
    parent = models.CharField(max_length=32)
    url = models.CharField(max_length=120,blank=True, null=True)
    icon = models.CharField(max_length=30, blank=True, null=True)
    sort = models.IntegerField()
    status = models.CharField(max_length=1)

    class Meta:
        verbose_name = u'菜单列表'
        verbose_name_plural = verbose_name


class RoleNav(models.Model):
    role = models.ForeignKey(Role,blank=True, null=True)
    nav = models.ForeignKey(Nav,related_name='navs',blank=True, null=True)

    class Meta:
        verbose_name = u'RoleNav'
        verbose_name_plural = verbose_name
        unique_together = (('role','nav'),)


class User(models.Model):
    name = models.CharField(max_length=45,verbose_name=u'用户名',unique=True)
    pwd = models.CharField(max_length=32,verbose_name=u'密码')
    nick = models.CharField(max_length=15,verbose_name=u'昵称',default='')
    depart = models.CharField(max_length=45,verbose_name=u'所属部门', blank=True, null=True)
    role = models.CharField(max_length=11,verbose_name=u'角色')
    status = models.CharField(max_length=1, verbose_name=u'状态',default='0')
    last_login = models.DateTimeField(blank=True, null=True,verbose_name=u'登陆时间')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name


class GiftCard(models.Model):
    name = models.CharField(max_length=12,verbose_name=u'名称-本地',default='礼品卡')
    title = models.CharField(max_length=12,verbose_name=u'名称-微信')
    wx_card_id = models.CharField(max_length=32,verbose_name=u'微信返回ID',blank=True,null=True)
    background_pic = models.CharField(max_length=128,verbose_name=u'背景图片')
    logo = models.CharField(max_length=128,verbose_name='logo')
    init_balance = models.DecimalField(max_digits=10, decimal_places=2,verbose_name=u'初始金额')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name=u'售价')
    brand_name = models.CharField(max_length=128, verbose_name='商户名称')
    quantity = models.IntegerField(verbose_name='库存数量')
    max_give = models.SmallIntegerField(verbose_name=u'最大赠送次数',default=9999)
    notice = models.CharField(verbose_name=u'使用提醒',max_length=12,default='')
    description = models.CharField(verbose_name=u'使用说明',max_length=1000,default='')
    status = models.CharField(max_length=1, verbose_name=u'状态(0:封存;1:禁用,2:启用,9:上线;)', default='2')
    # supply_bonus = models.CharField(max_length=1, verbose_name=u'支持积分',default='1')
    # supply_balance = models.CharField(max_length=1, verbose_name=u'支持余额',default='0')
    # auto_activate = models.CharField(max_length=1, verbose_name=u'自动激活',default='1')

    class Meta:
        verbose_name = u'礼品卡信息'
        verbose_name_plural = verbose_name
        db_table = 'gift_card'


class GiftImg(models.Model):
    title = models.CharField(max_length=12,verbose_name=u'名称')
    url = models.CharField(max_length=128,verbose_name=u'背景图片')
    create_time = models.DateField(max_length=128,verbose_name='创建日期',default=datetime.now)
    status = models.CharField(max_length=1,verbose_name=u'状态',default='0')

    class Meta:
        verbose_name = u'图片素材'
        verbose_name_plural = verbose_name
        db_table = 'gift_img'


class GiftTheme(models.Model):
    name = models.CharField(max_length=12,verbose_name=u'名称-本地',default='礼品卡')
    title = models.CharField(max_length=12,verbose_name=u'名称-微信')
    theme_pic = models.CharField(max_length=128, verbose_name=u'封面图片')
    title_color = models.CharField(max_length=7, verbose_name=u'主题字体颜色',default='#FB966E')
    sku_title_first = models.CharField(max_length=1, verbose_name=u'突出商品名(1:是,0:否)', default='0')
    create_time = models.DateField(max_length=128,verbose_name='创建日期',default=datetime.now)
    status = models.CharField(max_length=1, verbose_name=u'状态', default='0')
    is_banner = models.CharField(max_length=1, verbose_name=u'状态', default='0')
    class Meta:
        verbose_name = u'主题'
        verbose_name_plural = verbose_name
        db_table = 'gift_theme'


class GiftThemeItem(models.Model):
    theme_id = models.IntegerField(verbose_name=u'主题ID',default=1)
    wx_card_id = models.CharField(max_length=32, verbose_name=u'微信返回ID', blank=True, null=True)
    title = models.CharField(max_length=12, verbose_name=u'名称')

    class Meta:
        verbose_name = u'主题-item'
        verbose_name_plural = verbose_name
        db_table = 'gift_theme_item'


class GiftThemePicItem(models.Model):
    theme_id = models.IntegerField(verbose_name=u'主题ID',default=1)
    background_pic = models.CharField(max_length=128, verbose_name=u'背景图片')
    msg = models.CharField(max_length=32, verbose_name=u'默认祝福语')

    class Meta:
        verbose_name = u'主题-picItem'
        verbose_name_plural = verbose_name
        db_table = 'gift_theme_pic_item'


class GiftPage(models.Model):
    wx_page_id = models.CharField(max_length=128,verbose_name=u'微信返回货架ID',blank=True,null=True)
    title = models.CharField(max_length=12, verbose_name=u'货架名称')
    banner_pic = models.CharField(max_length=128, verbose_name=u'banner图片')
    categories = models.CharField(max_length=256, verbose_name=u'一级分类列表')
    themes = models.CharField(max_length=128, verbose_name=u'主题列表',default='')
    wx_page_url = models.CharField(max_length=128, verbose_name='货架首页地址',blank=True,null=True)

    class Meta:
        verbose_name = u'货架'
        verbose_name_plural = verbose_name
        db_table = 'gift_page'

class GiftCardCode(models.Model):
    wx_card_id = models.CharField(max_length=32,verbose_name=u'卡实例ID')
    code = models.CharField(max_length=12,verbose_name=u'线下Code',unique=True)
    status = models.CharField(max_length=1, default='0', verbose_name='code状态u(0:未销售;1:已销售)')
    class Meta:
        db_table = 'gift_card_code'


class GiftBalanceChangeLog(models.Model):
    last_serial = models.BigIntegerField(verbose_name='每次轮询的最后一个ID')
    create_time = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'gift_card_balance_change_log'


class GiftOrder(models.Model):
    order_id = models.CharField(max_length=32,verbose_name=u'订单号',unique=True)
    # page_id = models.CharField(max_length=64,verbose_name=u'货架号')
    trans_id = models.CharField(max_length=32,verbose_name=u'微信支付交易订单号')
    create_time = models.IntegerField(verbose_name=u'订单创建时间')
    pay_finish_time = models.IntegerField(verbose_name=u'订单支付时间')
    total_price = models.IntegerField(verbose_name='全部金额')
    open_id = models.CharField(max_length=32,verbose_name=u'购买者')

    class Meta:
        db_table = 'gift_order'

class GiftOrderInfo(models.Model):
    order_id = models.IntegerField(verbose_name=u'对应gift_order的自增长id')
    card_id = models.CharField(max_length=32,verbose_name=u'卡类型ID')
    price = models.IntegerField(verbose_name=u'卡面值')
    code = models.CharField(max_length=32,verbose_name=u'code',unique=True)

    class Meta:
        db_table = 'gift_order_info'


class ShopGood(models.Model):
    name = models.CharField(max_length=32,verbose_name=u'名称')
    sn = models.CharField(max_length=32,verbose_name=u'商品编码',unique=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u'价格')
    img = models.ImageField(upload_to='shop/%Y/%m', verbose_name=u'封面图', max_length=100)
    category = models.IntegerField(verbose_name=u'所属分类')
    stock = models.SmallIntegerField(verbose_name=u'库存',default=0)
    is_hot = models.CharField(max_length=1,verbose_name=u'热卖')
    is_new = models.CharField(max_length=1,verbose_name=u'新品')
    status = models.CharField(max_length=1,verbose_name=u'商品状态')
    save_time = models.DateTimeField(default=datetime.now,verbose_name=u'创建日期')

    class Meta:
        db_table = 'shop_good'


class ShopGoodImg(models.Model):
    good_sn = models.CharField(max_length=32,verbose_name=u'商品编码')
    img = models.ImageField(upload_to='shop/%Y/%m',verbose_name=u'商品编码',)
    sort = models.CharField(max_length=2,verbose_name=u'排序')

    class Meta:
        db_table = 'shop_good_img'


class ShopGoodProperty(models.Model):
    good_sn = models.CharField(max_length=32, verbose_name=u'商品编码')
    name = models.CharField(max_length=30, verbose_name=u'属性名')
    detail = models.CharField(max_length=255, verbose_name=u'属性值')
    sort = models.CharField(max_length=2, verbose_name=u'排序')

    class Meta:
        db_table = 'shop_good_property'


class ShopCategory(models.Model):
    name = models.CharField(max_length=32,verbose_name=u'名称')
    parent = models.IntegerField(verbose_name=u'父级分类')
    banner = models.ImageField(upload_to='shop/%Y/%m',verbose_name=u'banner图',null=True,blank=True)
    sort = models.CharField(max_length=2, verbose_name=u'排序', default=1)
    status = models.CharField(max_length=1,verbose_name=u'状态')

    class Meta:
        db_table = 'shop_category'


class ShopExpress(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'名称')
    tel = models.CharField(max_length=11,verbose_name=u'电话')
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u'价格')
    status = models.CharField(max_length=1, verbose_name=u'状态')

    class Meta:
        db_table = 'shop_express'


class ShopOrder(models.Model):
    sn = models.CharField(max_length=16,verbose_name=u'编号',unique=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name=u'价格')
    express = models.IntegerField(verbose_name=u'快递',blank=True,null=True)
    save_time = models.DateTimeField(default=datetime.now,verbose_name=u'下单时间')
    sign_time = models.DateTimeField(verbose_name=u'签收时间',blank=True,null=True)
    remark = models.TextField(verbose_name=u'备注留言',blank=True,null=True)
    address = models.CharField(max_length=12,verbose_name=u'配送地址ID',default='')
    customer = models.CharField(max_length=50, verbose_name=u'用户ID', default='0')
    status = models.CharField(max_length=1, verbose_name=u'订单状态',default='0')

    class Meta:
        db_table = 'shop_order'


class ShopOrderInfo(models.Model):
    order_sn = models.CharField(max_length=16, verbose_name='订单编号')
    good_sn= models.CharField(max_length=8,verbose_name='商品编码')
    good_num = models.IntegerField(verbose_name='商品数量')

    class Meta:
        db_table = 'shop_order_info'


class ShopTheme(models.Model):
    name = models.CharField(max_length=12, verbose_name=u'名称')
    desc = models.CharField(max_length=32,verbose_name=u'描述',blank=True,null=True)
    img = models.ImageField(upload_to='shop/%Y/%m',verbose_name=u'图片')
    banner = models.ImageField(upload_to='shop/%Y/%m',verbose_name=u'图片',default='')
    save_time = models.DateTimeField(default=datetime.now, verbose_name=u'更新时间')
    begin_time = models.DateTimeField(default=datetime.now, verbose_name=u'开始日期')
    end_time = models.DateTimeField(default=datetime.now, verbose_name=u'结束日期')
    sort = models.CharField(max_length=2, verbose_name=u'排序', default=1)


    class Meta:
        db_table = 'shop_theme'


class ShopThemeInfo(models.Model):
    theme_id = models.IntegerField()
    good_sn = models.CharField(max_length=8,verbose_name='商品编码')

    class Meta:
        db_table = 'shop_theme_info'
        unique_together=(('theme_id','good_sn'))


class ShopUser(models.Model):
    openid = models.CharField(max_length=50,verbose_name=u'',unique=True)
    nickname = models.CharField(max_length=10,verbose_name=u'昵称')
    extend = models.CharField(max_length=128,verbose_name=u'',default='')
    kg_money = models.IntegerField(default=0,verbose_name=u'宽广豆')
    create_time = models.DateTimeField(default=datetime.now,verbose_name=u'创建日期')

    class Meta:
        db_table = 'shop_user'


class ShopAddress(models.Model):
    openid = models.CharField(max_length=50,verbose_name=u'用户ID',default=0)
    name = models.CharField(max_length=12,verbose_name=u'收件人')
    tel = models.CharField(max_length=12,verbose_name=u'联系电话')
    province = models.CharField(max_length=12,verbose_name=u'省')
    city = models.CharField(max_length=12,verbose_name=u'市')
    country = models.CharField(max_length=12,verbose_name=u'县区')
    detail = models.CharField(max_length=50,verbose_name=u'详细地址',default='')
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u'')
    is_default = models.CharField(max_length=1,verbose_name=u'默认地址',default='0')

    class Meta:
        db_table = 'shop_address'


class ShopBanner(models.Model):
    name = models.CharField(max_length=16,verbose_name=u'')
    desc = models.CharField(max_length=32,verbose_name=u'',blank=True,null=True)
    save_time = models.DateTimeField(default=datetime.now, verbose_name=u'更新时间')
    status = models.CharField(max_length=1,verbose_name=u'')

    class Meta:
        db_table = 'shop_banner'


class ShopBannerInfo(models.Model):
    name = models.CharField(max_length=12,verbose_name=u'名称',default='')
    banner = models.IntegerField(default=0,verbose_name=u'bannerID')
    img = models.ImageField(upload_to='shop/%Y/%m',verbose_name=u'图片')
    type = models.CharField(max_length=1,verbose_name=u'类型（0:无导向;1:导向商品;2:导向专题）')
    target_id = models.IntegerField(verbose_name=u'跳转目标',blank=True,null=True)
    save_time = models.DateTimeField(default=datetime.now, verbose_name=u'更新时间')
    begin_time = models.DateTimeField( verbose_name=u'开始日期')
    end_time = models.DateTimeField(verbose_name=u'结束日期')
    sort = models.CharField(max_length=2, verbose_name=u'排序', default=1)

    class Meta:
        db_table = 'shop_banner_info'

