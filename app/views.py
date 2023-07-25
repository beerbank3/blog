from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from blog.models import Post
from django.utils.decorators import method_decorator
from blog.decorators import log_action
from django.core.paginator import Paginator
from django.db.models import Q

### index
@method_decorator(log_action(action='Index'), name='get')
class IndexMain(View):
    def get(self, request):
        category_name = request.GET.get('category', None)
        page = int(request.GET.get('page', 1))
        sort = request.GET.get('sort', 'reverse')

        q = Q(is_deleted=False)
        posts = Post.objects.filter(q).prefetch_related('categories').all()

        paginator = Paginator(posts , 6)

        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1

        page = paginator.get_page(page_number)

        context = {
            "posts": page,
            "title": "Travel Blog",
        }
        return render(request, 'index.html', context)