# -*- coding: utf_8 -*-
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章，分类，标签，侧边栏，友联的author字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('author', )

    # 重写ModelAdmin.save_model方法:保存数据到数据库中
    # obj是当前要保存的对象，form是页面提交过来的表单之后的对象，change用来标示本次保存的数据是新增还是修改
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super(BaseOwnerAdmin, self).get_queryset(request).filter(author=request.user)


