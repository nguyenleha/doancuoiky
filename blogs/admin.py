from django.contrib import admin

# Register your models here.
from blogs.models import Post, Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)