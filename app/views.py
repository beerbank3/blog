from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from blog.models import Post
from django.utils.decorators import method_decorator
from blog.decorators import log_action

### index
@method_decorator(log_action(action='Index'), name='get')
class IndexMain(View):
    def get(self, request):
                
        posts = Post.objects.prefetch_related('categories').all()
        context = {
            "posts": posts,
            "title": "Travel Blog",
        }
        return render(request, 'index.html', context)