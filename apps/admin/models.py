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
    url = models.CharField(max_length=120)
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
