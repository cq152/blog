import xadmin
from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Fieldset, Row, Container

from article.adminforms import PostAdminForm
from article.models import Category, Tag, Post
from blog.adminx import BaseOwnerAdmin


class PostInline:
    """ 同一个界面编辑两个model """
    form_layout = (
        Container(
            Row('title', 'summary')
        )
    )
    extra = 1
    model = Post


class CategoryAdmin(BaseOwnerAdmin):
    """
    1.继承BaseOwnerAdmin基类
    2.配置列表界面和编辑界面
    3.自定义函数：该分类下有多少文章
    """

    inlines = [PostInline, ]        # 关联PostInline

    # 查询列表显示的字段
    list_display = ['name', 'author', 'status', 'is_top', 'created_time', 'post_count']
    # 新增或者修改时现实的字段
    fields = ('name', 'status', 'is_top')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


xadmin.site.register(Category, CategoryAdmin)


class TagAdmin(BaseOwnerAdmin):
    """ 配置列表界面与编辑界面 """

    list_display = ['name', 'status', 'author', 'created_time']
    fields = ('name', 'status')


xadmin.site.register(Tag, TagAdmin)


class CategoryAuthorFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户分类 """
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(CategoryAuthorFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(author=request.user).values_list('id', 'name')


manager.register(CategoryAuthorFilter, take_priority=True)


class PostAdmin(BaseOwnerAdmin):

    form = PostAdminForm

    # <class 'article.admin.PostAdmin'>: (admin.E109) The value of 'list_display[3]' must not be a ManyToManyField.
    # list_display 不能包含ManyToMany字段
    list_display = ['title', 'author', 'category', 'summary', 'pv', 'uv', 'created_time', 'operator']
    list_filter = ['category']
    list_display_links = ['title', ]
    #  注意外键“分类”的编写
    search_fields = ['title', 'category__name']
    # 编辑页面不显示字段
    exclude = ['author', 'pv', 'uv']

    # 编辑界面
    # save_on_top = True

    # 'created_time' cannot be specified for Post model form as it is a non-editable field.
    # 'created_time' 不能出现在fields中，因为他是不可编辑字段
    # fields = (('category', 'title'), 'status', 'tag', 'summary', 'content')  替换为FieldsSet
    form_layout = (
        Fieldset(
            '基础信息',
            Row('category', 'title'),
            'status',
        ),
        Fieldset(
            '内容信息',
            'summary',
            'is_markdown',
            'content_ck',
            'content_md',
            'content'
        ),
        Fieldset(
            '额外信息',
            # 'classes': ('collapse',),
            'tag',
        )
    )

    # 多对多标签选择，水平显示
    filter_horizontal = ('tag', )
    # 多对多标签选择，垂直显示
    filter_vertical = ('tag', )

    # 自定义函数???
    def operator(self, obj):
        return format_html(
            '<a href="{0}"> 编辑 </a>',
            reverse('xadmin:article_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'


xadmin.site.register(Post, PostAdmin)
