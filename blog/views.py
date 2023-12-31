from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, UploadImage, User, Comment
from .decorators import log_action
from .forms import PostForm, CommentForm
from os.path import relpath
import os
# Create your views here.


### Post
@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Index'), name='get')
class Index(View):


    def get(self, request):
        category_name = request.GET.get('category', None)
        page_number = int(request.GET.get('page', 1))
        current_user_id = request.user.id
        q = Q(is_deleted=False)
        q &=Q(writer=current_user_id)
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
            "title": "My Blog",
            "categories" : categories,
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
        user_profile = request.user
    
        # 이미 게시글을 읽은 경우 중복 추가하지 않음
        if post not in user_profile.post_views.all():
            user_profile.post_views.add(post)
        post.views += 1
        post.save()
        comments = Comment.objects.filter(post_id=pk).order_by('created_at').all()

        context = {
            "title": "Blog Detail",
            'post_id': pk,
            'post_title': post.title,
            'post_writer': post.writer,
            'post_content': post.content,
            'post_views': post.views,
            'post_uploadfiles': post.upload_files,
            'post_categories' : post.categories.all(),
            'post_created_at': post.created_at.strftime('%Y-%m-%d'),
            'comments':comments
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


### Comment
@method_decorator(login_required, name='dispatch')
@method_decorator(log_action(action='Comment_Write'),name='dispatch')
class CommentWrite(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, pk=pk)

        if form.is_valid():
            content = form.cleaned_data['content']
            writer = request.user

            try:
                comment = Comment.objects.create(post=post, content=content, writer=writer)
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            except ValidationError as e:
                print('Valdation error occurred', str(e))
            
            return redirect('blog:detail', pk=pk)
        
        context = {
            "title": "Blog",
            'post_id': pk,
            'comments': post.comment_set.all(),
            'comment_form': form,
        }
        return render(request, 'blog/post_detail.html', context)


class CommentDelete(View):
    
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        
        post_id = comment.post.id

        comment.delete()
        
        return redirect('blog:detail', pk=post_id)
    
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