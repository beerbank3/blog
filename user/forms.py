from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import User
from django.contrib.auth import get_user_model
from blog.models import Category
from .models import User


User = get_user_model()


class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['email']


class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # 변경된 이름과 기존 이름이 같을 때는 중복 검사를 하지 않고 통과
        if self.instance and self.instance.name == name:
            return name
        # 중복된 이름이 있는지 확인
        if User.objects.filter(name=name).exists():
            # 중복된 이름이 있다면 오류 발생
            raise forms.ValidationError("이미 사용 중인 이름입니다.")
        return name
        
    name = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=False)
    profile_image = forms.FileField(required=False)
    categories = forms.MultipleChoiceField(
        choices=Category.objects.all().values_list('id', 'name'),  # 카테고리 선택지를 가져와 사용
        widget=forms.MultipleHiddenInput,
        required=False
    )
    class Meta:
        model = User
        fields = ['name', 'content', 'profile_image', 'categories']