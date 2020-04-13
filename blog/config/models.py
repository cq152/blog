# -*- coding:utf-8 -*-
import json

from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from pip._vendor import requests


class SidePane(models.Model):

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = [
        (STATUS_HIDE, '隐藏'),
        (STATUS_SHOW, '展示')
    ]

    TYPE_NORMAL = 0
    TYPE_HOT = 1
    TYPE_RECENT = 2
    TYPE_COMMENTS = 3
    TYPE_ITEMS = [
        (TYPE_NORMAL, '每日一句'),
        (TYPE_HOT, '最热文章'),
        (TYPE_RECENT, '最新文章'),
        (TYPE_COMMENTS, '最新评论')
    ]

    title = models.CharField(max_length=50, verbose_name='标题')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_SHOW, verbose_name='展示状态')
    type = models.PositiveIntegerField(choices=TYPE_ITEMS, default=TYPE_NORMAL, verbose_name='文章类型')
    content = models.CharField(max_length=500, blank=True, verbose_name='内容', help_text='如果设置的不是HTML类型，可为空')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
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

    @property
    def display_html(self):
        """ 直接渲染模板 """
        from article.models import Post
        from comment.models import Comment

        result = ''
        if self.type == self.TYPE_NORMAL:
            # result = self.content
            # 添加每日一句
            result = self.get_chicken_soup()
        elif self.type == self.TYPE_RECENT:
            context = {'posts': Post.get_latest_posts()}
            result = render_to_string('config/block/sidebar_posts.html', context)
        elif self.type == self.TYPE_HOT:
            context = {'posts': Post.get_hottest_posts()}
            result = render_to_string('config/block/sidebar_posts.html', context)
        elif self.type == self.TYPE_COMMENTS:
            context = {'comments': Comment.get_recently_comments()}
            result = render_to_string('config/block/sidebar_comments.html', context)

        return result

    @staticmethod
    def get_chicken_soup():
        """ 获取金山词霸的中英文每日一句 """
        url = 'http://open.iciba.com/dsapi/'        # 金山词霸免费开放的jsonAPI借口
        req = requests.get(url)
        req_text = json.loads(req.text)
        english_text = req_text['content']
        chinese_text = req_text['note']
        soup = english_text + "<br/>" + chinese_text
        return soup


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
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name='权重',
                                         help_text='权重高显示靠前')
    desc = models.CharField(max_length=255, default='', verbose_name='描述')

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.name







