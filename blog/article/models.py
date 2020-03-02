# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


'''
须先定义分类及标签，随后在文章类中作为成员属性
'''

class Category(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除')
    ]

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.IntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    is_top = models.BooleanField(default=False,verbose_name='是否置顶导航')

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    ]

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.IntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_DELETE,'删除'),
        (STATUS_NORMAL,'正常'),
        (STATUS_DRAFT,'草稿')
    ]

    title = models.CharField(max_length=255, verbose_name='标题')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    summmary = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(help_text='正文必须为MarkDown格式', verbose_name='正文')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    # auto_now_add 创建时赋值，auto_now 更新时赋值
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']      # 降序显示


