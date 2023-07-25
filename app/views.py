from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from blog.models import Post
from django.utils.decorators import method_decorator
from blog.decorators import log_action
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Category

### index
@method_decorator(log_action(action='Index'), name='get')
class IndexMain(View):
    def get(self, request):
        category_name = request.GET.get('category', None)
        page_number = int(request.GET.get('page', 1))

        q = Q(is_deleted=False)
        if category_name:
            q &= Q(categories__name=category_name)
        posts = Post.objects.filter(q).prefetch_related('categories').all()

        paginator = Paginator(posts , 6)

        if not page_number:
            page_number = 1

        page = paginator.get_page(page_number)
        categories = Category.objects.all()
        context = {
            "posts": page,
            "title": "Travel Blog",
            "categories": categories
        }
        return render(request, 'index.html', context)