from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)
    upload_files = forms.FileField(required=False)
    categories = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'upload_files', 'categories']