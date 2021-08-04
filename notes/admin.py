from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'author', 'category', 'created_at', 'published', 'photo']
    list_filter = ['published', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
