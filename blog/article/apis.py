# -*- coding: utf_8 -*-
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from article.models import Post, Category
from article.serializers import PostSerializer, PostDetailSerializer, CategorySerializer


# 测试function view和class-based view
# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)
#
#
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)






