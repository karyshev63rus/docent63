from django.urls import path
from .views import *


app_name = 'notes'

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('reversed_posts/', reversed_post_list, name='reversed_post_list'),
    path('search/', post_search, name='post_search'),
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('categories/<slug:category_slug>/', post_list, name='category_post_list'),
    path('tags/<slug:tag_slug>/', post_list, name='tag_post_list'),
    path('', portal, name='portal'),
]
