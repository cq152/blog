from django.contrib import admin

# Register your models here.
from blog.base_admin import BaseOwnerAdmin
from blog.customsite import custom_site
from comment.models import Comment


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ['content', 'status', 'created_time', ]


