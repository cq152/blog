from django.contrib import admin

# Register your models here.
from blog.base_admin import BaseOwnerAdmin
from blog.customsite import custom_site
from config.models import Link, SidePane


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['name', 'link', 'status', 'author', 'created_time']
    fields = ['name', 'link', 'status', 'weight']


@admin.register(SidePane, site=custom_site)
class SidePaneAdmin(BaseOwnerAdmin):
    list_display = ['title', 'status', 'type', 'author']

    fields = ['title', 'content', 'status']
