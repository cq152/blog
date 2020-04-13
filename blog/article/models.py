# -*- coding:utf-8 -*-
import mistune
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
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)
    is_top = models.BooleanField(default=False, verbose_name='是否置顶导航')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_top(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        """
        直接从数据库取值,耗费数据库链接查询资源
        top_categories = categories.filter(is_top=True)
        normal_categories = categories.filter(is_top=False)
        """

        """
        列表推导式, 两次for循环
        top_categories = [cate for cate in categories if cate.is_top]
        normal_categories = [cate for cate in categories if not cate.is_top]
        """

        # 一次for循环
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
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
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
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.DO_NOTHING)
    # 多对多
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    summary = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(help_text='正文必须为MarkDown格式', verbose_name='正文')
    content_html = models.TextField(verbose_name='正文_html', blank=True, editable=False)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    # auto_now_add 创建时赋值，auto_now 更新时赋值
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)

    # 新增字段pv和uv，方便最热文章与最活跃用户的取数
    pv = models.PositiveIntegerField(default=0)
    uv = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']      # 降序显示

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.content_html = mistune.markdown(self.content)
        super(Post, self).save()

    @staticmethod
    def get_by_tag(tag_id):
        """ 通过标签得到文章 """
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
        """ 通过分类得到文章 """
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
        """ 得到最新10篇文章 """
        latest_posts = cls.objects.filter(status=cls.STATUS_NORMAL)[:5:1]
        return latest_posts

    @classmethod
    def get_hottest_posts(cls):
        """ 得到最热10篇文章 """
        hottest_posts = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:5:1]
        return hottest_posts

#
# class ArticlePostTag(models.Model):
#     post = models.ForeignKey(Post, models.DO_NOTHING)
#     tag = models.ForeignKey(Tag, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'article_post_tag'
#         unique_together = (('post', 'tag'),)


