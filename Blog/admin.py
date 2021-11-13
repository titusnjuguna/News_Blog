from django.contrib import admin
from .models import Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'body', 'active', 'created')
    list_filter = ('active', 'updated', 'created')
    search_fields = ('name', 'email', 'body')
