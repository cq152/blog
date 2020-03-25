from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from article.adminforms import PostAdminForm
from article.models import Category, Tag, Post
from blog.base_admin import BaseOwnerAdmin
from blog.customsite import custom_site


class PostInline(admin.TabularInline):
    """ 同一个界面编辑两个model """

    fields = ('title', 'summary')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)         # 自配置site
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


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    """ 配置列表界面与编辑界面 """

    list_display = ['name', 'status', 'author', 'created_time']
    fields = ('name', 'status')


class CategoryAuthorFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = "分类过滤器"
    parameter_name = "owner_category"

    # 重写
    def lookups(self, request, model_admin):
        return Category.objects.filter(author=request.user).values_list("id", "name")

    # 重写
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):

    form = PostAdminForm

    # <class 'article.admin.PostAdmin'>: (admin.E109) The value of 'list_display[3]' must not be a ManyToManyField.
    # list_display 不能包含ManyToMany字段
    list_display = ['title', 'author', 'category', 'summary', 'content', 'status', 'created_time', 'operator']
    list_filter = [CategoryAuthorFilter, 'author']
    list_display_links = ['title', ]
    #  注意外键“分类”的编写
    search_fields = ['title', 'category__name']

    # 编辑界面
    # save_on_top = True

    # 'created_time' cannot be specified for Post model form as it is a non-editable field.
    # 'created_time' 不能出现在fields中，因为他是不可编辑字段夏先生
    # fields = (('category', 'title'), 'status', 'tag', 'summary', 'content')  替换为FieldsSet
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (('category', 'title'), 'status')
        }),
        ('内容', {
            'fields': ('summary', 'content')
        }),
        ('额外信息', {
            # 'classes': ('collapse',),
            'fields': ('tag',)
        })
    )

    # 多对多标签选择，水平显示
    filter_horizontal = ('tag', )
    # 多对多标签选择，垂直显示
    # filter_vertical = ('tag', )

    # 自定义函数???
    def operator(self, obj):
        return format_html(
            '<a href="{0}"> 编辑 </a>',
            reverse('cus_admin:article_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', )
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']


