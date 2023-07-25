from django.db import models
from django.contrib.auth import get_user_model
import base64
import os

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_files = models.ImageField(upload_to="image/", null=True)
    views = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'[{self.post}] {self.content} :: {self.writer}'

    def get_absolute_url(self):
        return f'/blog/{self.post.pk}/#comment-{self.pk}'

    class Meta:
        ordering = ['-id']


class UploadImage(models.Model):
    image = models.ImageField(upload_to='images/')
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 이미지 파일 이름을 base64로 인코딩하여 저장합니다.
        encoded_name = base64.b64encode(os.path.basename(self.image.path).encode('utf-8')).decode('utf-8')
        new_name = f'{encoded_name}.{self.image.name.split(".")[-1]}'
        os.rename(self.image.path, os.path.join(os.path.dirname(self.image.path), new_name))
        self.image.name = new_name

    def __str__(self):
        return self.image.name
    

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=200, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {self.action}"