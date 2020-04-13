from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
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

    # 由comment的templatetags封装，此处不再需要渲染
    # def get_context_data(self, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path)
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)      # 缓存一分钟有效,cache.set(key,value,timeout)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 缓存24小时有效

        if increase_pv and increase_uv:
            Post.objects.filter(id=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(id=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(id=self.object.id).update(uv=F('uv') + 1)


class SearchView(BasePostView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update(
            {'keyword': self.request.GET.get('keyword', '')}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(summary__icontains=keyword))


class AuthorView(BasePostView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('author_id')
        return queryset.filter(author_id=author_id)
