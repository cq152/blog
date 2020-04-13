import xadmin

# Register your models here.
from blog.adminx import BaseOwnerAdmin
from config.models import Link, SidePane


class LinkAdmin(BaseOwnerAdmin):
    list_display = ['name', 'link', 'status', 'author', 'created_time']
    fields = ['name', 'link', 'status', 'weight', 'desc']


xadmin.site.register(Link, LinkAdmin)


class SidePaneAdmin(BaseOwnerAdmin):
    list_display = ['title', 'status', 'type', 'author']

    fields = ['title', 'content', 'status', 'type']


xadmin.site.register(SidePane, SidePaneAdmin)

