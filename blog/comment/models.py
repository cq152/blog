# -*- coding:utf-8 -*-

from django.db import models

# Create your models here.
from article.models import Post


class Comment(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    ]

    target = models.CharField(max_length=500, verbose_name='评论目标')      # 方便存储多对象
    # target = models.ForeignKey(Post, verbose_name='评论目标', on_delete=models.CASCADE)       # 只能存储屏障的ID
    content = models.CharField(max_length=1000, verbose_name='内容')
    author = models.CharField(max_length=50, verbose_name='昵称')
    site = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ['-id']      # 降序显示

    def __str__(self):
        return self.content

    @classmethod
    def get_recently_comments(cls):
        """ 得到最近评论 """
        recently_comments = cls.objects.filter(status=cls.STATUS_NORMAL)[:10:1]
        return recently_comments

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)



