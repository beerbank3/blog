from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from blog.models import Post


### index
class IndexMain(View):
    def get(self, request):
                
        posts = Post.objects.prefetch_related('categories').all()
        context = {
            "posts": posts,
            "title": "Travel Blog",
        }
        return render(request, 'index.html', context)