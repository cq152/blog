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

    target = models.ForeignKey(Post, verbose_name='评论目标', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    site = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ['-id']      # 降序显示

    def __str__(self):
        return self.content



