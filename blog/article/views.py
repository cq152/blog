from django.views.generic import ListView
from django.views.generic import DetailView

from article.models import Tag, Post, Category
from config.models import SidePane


class CommonMixin(object):
    def get_context_data(self, **kwargs):
        # 方法一
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context.update(Category.get_top())
        context.update(SidePane.get_show())
        return context

        # 方法二
        # context = Category.get_top()
        # context.update(SidePane.get_show())
        # return super(CommonMixin, self).get_context_data(**context)


class BasePostView(CommonMixin, ListView):
    model = Post
    template_name = 'article/list.html'
    context_object_name = 'post_list'
    paginate_by = 4


class PostListView(BasePostView):
    pass


class CategoryView(BasePostView):
    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)

        return qs


class TagView(BasePostView):
    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = []
        qs = tag.post_set.all()

        return qs


class PostDetailView(CommonMixin, DetailView):
    model = Post
    template_name = 'article/detail.html'
    context_object_name = 'post'
