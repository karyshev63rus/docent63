from django import template
from django.db.models import Count
from notes.models import Category, Post, Tag, Comment


register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def get_latest_posts():
    return Post.objects.all()[:3]


@register.simple_tag
def get_most_recommended_posts():
    most_recommended_posts = Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]
    return most_recommended_posts
