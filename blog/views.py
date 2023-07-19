from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from os.path import relpath
from .models import Post, UploadImage
from .forms import PostForm
import os
# Create your views here.


### Post
@method_decorator(login_required, name='dispatch')
class Index(View):
    
    def get(self, request):
        posts = Post.objects.prefetch_related('categories').all()
        context = {
            "posts": posts,
            "title": "My Blog",
        }
        return render(request, 'blog/index.html', context)
    

### Write
@method_decorator(login_required, name='dispatch')
class Write(LoginRequiredMixin, View):
    
    def get(self, request):
        user = request.user
        form = PostForm()
        context = {
            'form': form,
            "title": "Blog",
            "user": user
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            return redirect('blog:list')
        
        context = {
            'form': form
        }
        
        return render(request, 'blog/post_form.html', context)
    

### Detail
@method_decorator(login_required, name='dispatch')
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
            'post_created_at': post.created_at.strftime('%Y-%m-%d')
        }
        
        return render(request, 'blog/post_detail.html', context)


### Upload_Image
@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('images'):
        image_file = request.FILES['images']
        writer = request.user
        upload_image = UploadImage(image=image_file, writer=writer)
        upload_image.save()

        image_path = os.path.relpath(upload_image.image.path, settings.MEDIA_ROOT)

        response_data = {'message': '이미지가 성공적으로 업로드되었습니다.', 'image_path': '/blog/media/images/'+image_path}
        return JsonResponse(response_data)
    else:
        response_data = {'message': '이미지 업로드에 실패했습니다.'}
        return JsonResponse(response_data, status=400)