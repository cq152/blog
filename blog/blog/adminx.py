# -*- coding: utf_8 -*-


class BaseOwnerAdmin(object):
    """
    1.用来自动补充文章，分类，标签，侧边栏，友联的author字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('author', )

    # 重写ModelAdmin.save_model方法:保存数据到数据库中
    # new_obj是当前要保存的对象

    def get_list_queryset(self):
        request = self.request
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        return qs.filter(author=request.user)

    def save_models(self):
        # 防止超级管理员修改文章导致文章原作者被修改
        if not self.org_obj:
            self.new_obj.author = self.request.user
        return super(BaseOwnerAdmin, self).save_model()


