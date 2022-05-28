from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'content',
        'post_type',
        'has_media',
        'edited',
        'created_at',
        'updated_at'
    )
    list_filter = ['author', 'post_type', 'has_media', 'edited']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'post',
        'content',
        'edited',
        'created_at',
        'updated_at'
    )
    list_filter = ['author', 'edited']
