from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = RichTextField(blank=True,null=True)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='blogs.images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detailpost', args=[str(self.id)])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name="users",on_delete=models.CASCADE,default=None, null=True,blank=True)
    name = models.CharField(max_length=250)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    