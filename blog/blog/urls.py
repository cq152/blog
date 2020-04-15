"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import ckeditor_uploader
import xadmin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.urls import include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from article.apis import PostViewSet, CategoryViewSet
from article.views import PostListView, PostDetailView, CategoryView, TagView, SearchView, AuthorView
from comment.views import CommentView
from config.views import LinkView
from blog import adminx    # NOQA

xadmin.autodiscover()
router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')


urlpatterns = [
    url(r'^$', PostListView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag'),
    url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name='detail'),
    url(r'^links/$', LinkView.as_view(), name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # url(r'^api/post/', post_list, name='post-list'),
    # url(r'^api/post/', PostList.as_view(), name='post-list'),
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', include_docs_urls(title="cq's blog apis")),

    url(r'^admin/', xadmin.site.urls, name='xadmin')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
