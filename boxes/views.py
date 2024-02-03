from django.shortcuts import render
from django.views.generic import DetailView
from .models import BoxContents


class BoxContentsDetailView(DetailView):
    model = BoxContents
    template_name = 'boxes/box_contents_detail.html'
