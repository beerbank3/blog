from django.shortcuts import render
from django.views import View
from .models import Post
# Create your views here.
### Post
class Index(View):
    
    def get(self, request):
        posts = Post.objects.prefetch_related('categories').all()
        context = {
            "posts": posts,
            "title": "My Blog"
        }
        return render(request, 'blog/index.html', context)
    

class DetailView(View):
    
    def get(self, request, pk):
        post = Post.objects.prefetch_related('categories').get(pk=pk)
        
        context = {
            "title": "Blog Detail",
            'post_id': pk,
            'post_title': post.title,
            'post_writer': post.writer,
            'post_content': post.content,
            'post_uploadfiles': post.upload_files,
            'post_categories' : post.categories.all(),
            'post_created_at': post.created_at.strftime('%Y-%m-%d'),
        }
        
        return render(request, 'blog/post-detail.html', context)