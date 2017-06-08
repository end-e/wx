from django.db import models


class Voucher(models.Model):
    voucher_no = models.CharField(max_length=32, default='', verbose_name=u'优惠码')
    voucher_name = models.CharField(max_length=32, default='', verbose_name=u'商品名称')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=u'原价')
    voucher_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'优惠价')
    goods_code = models.CharField(max_length=32, default='', verbose_name=u'商品码')
    begin_date = models.DateTimeField(blank=True, null=True, verbose_name=u'开始日期')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'截至日期')
    type_flag = models.CharField(max_length=2, default='0', verbose_name=u'类型 0通用 1微信专享')
    code_flag = models.CharField(max_length=2, default='0', verbose_name=u'门店范围 0全部 1市区 2县区 3自由')
    shop_codes = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'适用门店')
    voucher_image = models.ImageField(upload_to='upload', blank=True, null=True, verbose_name=u'券图片')


class PosterImage(models.Model):
    poster_name = models.CharField(max_length=32, default='', verbose_name=u'海报名称')
    begin_date = models.DateTimeField(blank=True, null=True, verbose_name=u'开始日期')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'截至日期')
    poster_image = models.ImageField(upload_to='upload', blank=True, null=True, verbose_name=u'海报图片')


class Product(models.Model):
    product_code = models.CharField(max_length=32, default='', verbose_name=u'商品编号')
    product_name = models.CharField(max_length=32, default='', verbose_name=u'商品名称')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u'单价')
    stock = models.IntegerField(default=0, verbose_name=u'库存')
    type_flag = models.CharField(max_length=2, default='0', verbose_name=u'类型 0普通换购商品 1心愿商品')
    enable_flag = models.CharField(max_length=2, default='0', verbose_name=u'可用标记 0可用 1禁用')
    begin_date = models.DateTimeField(blank=True, null=True, verbose_name=u'开始日期')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=u'截至日期')
    product_weight = models.DecimalField(max_digits=12, decimal_places=5, verbose_name=u'商品重量 单位千克')
    product_image = models.ImageField(upload_to='upload/product', blank=True, null=True, verbose_name=u'商品图')


class Shops(models.Model):
    shop_code = models.CharField(max_length=16, default='', verbose_name=u'编号')
    shop_name = models.CharField(max_length=32, default='', verbose_name=u'名称')
    telphone = models.CharField(max_length=20, default='', verbose_name=u'电话')
