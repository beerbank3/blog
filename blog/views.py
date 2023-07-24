from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from os.path import relpath
from .models import Post, Category, UploadImage, User
from .decorators import log_action
from .forms import PostForm, CommentForm
import os
# Create your views here.


### Post
@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Index'), name='dispatch')
class Index(View):
    
    def get(self, request):
        current_user_id = request.user.id
        posts = Post.objects.filter(writer=current_user_id).prefetch_related('categories').all()
        context = {
            "posts": posts,
            "title": "My Blog",
        }
        return render(request, 'blog/index.html', context)
    

### Write
@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Post_Write'),name='dispatch')
class Write(View):
    
    def get(self, request):
        user = request.user
        categories = Category.objects.all()
        form = PostForm()
        context = {
            "form": form,
            "title": "Blog",
            "user": user,
            "categories" : categories
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        categories = Category.objects.all()
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.upload_files = form.cleaned_data['upload_files']
            post.save()
            post.categories.set(form.cleaned_data['categories'])
            return redirect('blog:list')
        
        context = {
            'form': form,
            "categories" : categories
        }
        
        return render(request, 'blog/post_form.html', context)
    

### Detail
@method_decorator(log_action(action='Post_View'),name='dispatch')
class DetailView(View):
    
    def get(self, request, pk):
        post = Post.objects.prefetch_related('categories').get(pk=pk)
        user_profile = User.objects.get(user=request.user)
    
        # 이미 게시글을 읽은 경우 중복 추가하지 않음
        if post not in user_profile.post_views.all():
            user_profile.post_views.add(post)
        post.views += 1
        post.save()
        context = {
            "title": "Blog Detail",
            'post_id': pk,
            'post_title': post.title,
            'post_writer': post.writer,
            'post_content': post.content,
            'post_views': post.views,
            'post_uploadfiles': post.upload_files,
            'post_categories' : post.categories.all(),
            'post_created_at': post.created_at.strftime('%Y-%m-%d')
        }
        
        return render(request, 'blog/post_detail.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Post_Update'),name='dispatch')
class Update(View):
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        categories = Category.objects.all()
        form = PostForm(initial={'title': post.title, 'content': post.content, 'upload_files':post.upload_files,'categories':post.categories})
        context = {
            'form': form,
            'post': post,
            'categories' : categories,
            "title": "Blog"
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            if not request.FILES.get('upload_files'):
                form.cleaned_data['upload_files'] = post.upload_files
            post.upload_files = form.cleaned_data['upload_files']
            post.categories.set(form.cleaned_data['categories'])
            post.save()
            return redirect('blog:detail', pk=pk)
        
        context = {
            'form': form,
            "title": "Blog"
        }
        
        return render(request, 'blog/post_edit.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Post_Delete'),name='dispatch')
class Delete(View):
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('blog:list')


@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Comment_Write'),name='dispatch')
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                # commit=False를 하면, DB에 바로 저장되지 않습니다.
                # 대신, 메모리에 Comment 객체를 하나 생성해 줍니다.
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


### Upload_Image
@login_required
@method_decorator(log_action(action='Upload_image'),name='dispatch')
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