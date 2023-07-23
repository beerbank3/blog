from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)
    upload_files = forms.FileField(required=False)
    categories = forms.MultipleChoiceField(
        choices=Category.objects.all().values_list('id', 'name'),  # 카테고리 선택지를 가져와 사용
        widget=forms.MultipleHiddenInput,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'upload_files', 'categories']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']