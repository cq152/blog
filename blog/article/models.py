# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    须先定义分类及标签，随后在文章类中作为成员属性
    """

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    ]

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.IntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)
    is_top = models.BooleanField(default=False, verbose_name='是否置顶导航')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_top(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        top_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_top:
                top_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'top_categories': top_categories,
            'normal_categories': normal_categories
        }


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
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_DELETE, '删除'),
        (STATUS_NORMAL, '正常'),
        (STATUS_DRAFT, '草稿')
    ]

    title = models.CharField(max_length=255, verbose_name='标题')
    # 多对一
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # 多对多
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    summary = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(help_text='正文必须为MarkDown格式', verbose_name='正文')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    # auto_now_add 创建时赋值，auto_now 更新时赋值
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    # 新增字段pv和uv，方便最新和最热文章的取数
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']      # 降序显示

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            posts = []
        else:
            posts = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('author', 'category')

        return posts, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            posts = []
        else:
            posts = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('author', 'category')

        return posts, category

    @classmethod
    def get_latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)

        return queryset

    @classmethod
    def get_hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')


