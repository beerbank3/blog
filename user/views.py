from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

# from .models import User
from .forms import RegisterForm, LoginForm, UserProfileForm
from blog.models import Category

### Registration
class Registration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        # 회원가입 페이지
        form = RegisterForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'user/user_register.html', context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        else:
            errors = form.errors
            return render(request, 'user/user_register.html', {'form': form, 'errors': errors})

### Login
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm()
        context = {
            'form': form,
            'title': 'User'
        }
        return render(request, 'user/user_login.html', context)
        
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password) # True, False
            
            if user:
                login(request, user)
                return redirect('blog:list')
            
        # form.add_error(None, '아이디가 없습니다.')
        
        context = {
            'form': form
        }
        
        return render(request, 'user/user_login.html', context)


### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    

class ProfileUpdate(View):

    def get(self, request):
        categories = Category.objects.all()
    
        user = request.user
        form = UserProfileForm()
        context = {
            'form': form,
            "title": f"{user.name} Profile",
            'user': user,
            "categories" : categories
        }
        return render(request, 'user/user_update.html', context)

    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.name = form.cleaned_data.get('name')
            user.content = form.cleaned_data.get('content')
            user.profile_image = form.cleaned_data.get('profile_image')
            user.categories.set(form.cleaned_data['categories'])
            user.save()
            
            return redirect('blog:list')