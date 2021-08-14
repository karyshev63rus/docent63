from django.contrib import admin
from .models import Post, Category, Tag, Comment, Slide, SlideTextItem


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


class SlideTextItemInline(admin.TabularInline):
    model = SlideTextItem


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'text', 'link', 'target', 'picture')
    list_editable = ('text', 'subtitle', 'link', 'target')

    inlines = [SlideTextItemInline]
