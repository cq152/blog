# -*- coding: utf_8 -*-
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from article.models import Post, Category


class PostSerializer(ModelSerializer):

    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format("%Y-%m-%d %H:%M:%S"))

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'author', 'created_time']


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'author', 'created_time', 'content_html']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time']


