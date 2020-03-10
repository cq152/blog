# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class SidePane(models.Model):

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = [
        (STATUS_HIDE,'隐藏'),
        (STATUS_SHOW,'展示')
    ]

    TYPE_NORMAL = 0
    TYPE_HOT = 1
    TYPE_RECENT = 2
    TYPE_COMMENTS = 3
    TPTE_ITEMS = [
        (TYPE_NORMAL,'HTML'),
        (TYPE_HOT,'最热文章'),
        (TYPE_RECENT,'最新文章'),
        (TYPE_COMMENTS,'最多评论')
    ]

    title = models.CharField(max_length=50, verbose_name='标题')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_SHOW, verbose_name='展示状态')
    type = models.PositiveIntegerField(choices=TPTE_ITEMS, default=TYPE_NORMAL, verbose_name='文章类型')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容', help_text='如果设置的不是HTML类型，可为空')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    def __str__(self):
        return self.title

    @classmethod
    def get_show(cls):
        sides = cls.objects.filter(status=cls.STATUS_SHOW)

        return {
            'sides': sides
        }


class Link(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    ]

    name = models.CharField(max_length=50, verbose_name='标题')
    link = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)
    weight = models.PositiveIntegerField(default=1,choices=zip(range(1,6), range(1,6)), verbose_name='权重',
                                         help_text='权重高显示靠前')

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.name







