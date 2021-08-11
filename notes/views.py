from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Post
from .forms import CommentForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def portal(request):
    posts = Post.objects.all()
    return render(request,
                  'portal.html', {'posts': posts})


def post_list(request, category_slug=None, tag_slug=None, reversed_list=False):
    if category_slug:
        posts_list = Post.objects.filter(category__slug=category_slug)
    elif tag_slug:
        posts_list = Post.objects.filter(tag__slug=tag_slug)
    elif reversed_list:
        posts_list = Post.objects.all()[::-1]
    else:
        posts_list = Post.objects.all()
    page_content = paginate(request, posts_list, 3)
    return render(request,
                  'notes/list.html',
                  {'posts': page_content})


def reversed_post_list(request):
    return post_list(request, reversed_list=True)


def paginate(request, raw_content, items_on_page):
    paginator = Paginator(raw_content, items_on_page)
    page = request.GET.get('page')
    try:
        page_content = paginator.page(page)
    except PageNotAnInteger:
        page_content = paginator.page(1)
    except EmptyPage:
        page_content = paginator.page(paginator.num_pages)
    return page_content


def post_detail(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    comments = post.comments.filter(active=True).order_by('-created')
    page_content = paginate(request, comments, 5)
    total_comments = comments.count
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.save()
        return redirect('notes:post_detail', post_slug=post_slug)
    else:
        comment_form = CommentForm()
    ordered_similar_posts = get_similar_posts(post, 3)
    return render(request,
                  'notes/detail.html',
                  {'post': post,
                   'comments': page_content,
                   'total_comments': total_comments,
                   'comment_form': comment_form,
                   'ordered_similar_posts': ordered_similar_posts,
                   'to_post_list_page': True})


def get_similar_posts(post, num_of_posts):
    post_tags_id = post.tag.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tag__in=post_tags_id).exclude(id=post.id)
    ordered_similar_posts = similar_posts.annotate(
            same_tags=Count('tag')
        ).order_by('-same_tags', '-published')[:num_of_posts]
    return ordered_similar_posts


def post_search(request):
    query = request.GET.get('query')
    results = []
    if query is not None:
        results = Post.objects.annotate(
            search=SearchVector('title', 'body'),
        ).filter(search=query)
    return render(request,
                  'notes/search.html',
                  {'query': query,
                   'results': results,
                   'to_post_list_page': True})
