from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from article.views import CommonMixin
from config.models import Link


class LinkView(CommonMixin, ListView):
    # model = Link
    template_name = 'config/links.html'
    context_object_name = 'links'
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
