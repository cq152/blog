from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from article.models import Tag, Post, Category
from config.models import SidePane


def post_list(request, category_id=None, tag_id=None):
    # 测试代码１
    # content = 'post_list category_id={0},　tag_id={1}'.format(category_id, tag_id)
    # return HttpResponse(content)

    # 测试代码２
    # return render(request, 'article/list.html', context={'name': 'post_list'})
    tag = None
    category = None
    page = request.GET.get('page', 1)
    page_size = 4
    try:
        page = int(page)
    except TypeError:
        page = 1

    if tag_id:
        posts, tag = Post.get_by_tag(tag_id)
    elif category_id:
        posts, category = Post.get_by_category(category_id)
    else:
        posts = Post.get_latest_posts()

    # 分页
    paginator = Paginator(posts, page_size)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'post_list': posts,
        'tag': tag,
        'category': category
    }

    context.update(Category.get_top())
    context.update(SidePane.get_show())

    return render(request, 'article/list.html', context=context)


def post_detail(request, post_id=None):
    # 测试代码１
    # content = 'post_detail post_id = {0}'.format(post_id)
    # return HttpResponse(content)

    # 测试代码２
    # return render(request, 'article/detail.html', context={'name': 'post_detail'})

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {'post': post}

    context.update(Category.get_top())
    context.update(SidePane.get_show())

    return render(request, 'article/detail.html', context=context)
