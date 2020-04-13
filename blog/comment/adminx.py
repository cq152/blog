import xadmin

# Register your models here.
from blog.adminx import BaseOwnerAdmin
from comment.models import Comment


class CommentAdmin(BaseOwnerAdmin):
    list_display = ['content', 'status', 'created_time', ]


xadmin.site.register(Comment, CommentAdmin)
