from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post', verbose_name='автор')
    title = models.CharField(max_length=32, verbose_name='заголовок')
    slug = models.SlugField(max_length=32, unique=True, verbose_name='слаг')
    body = models.TextField(blank=True, verbose_name='текст')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлено')
    published = models.BooleanField(default=False, verbose_name='опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='posts',
                                 verbose_name='рубрика')
    tag = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='тег')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'статью'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:post_detail', args=[self.slug])


class Category(models.Model):
    title = models.CharField(max_length=32, db_index=True, verbose_name='рубрика')
    slug = models.SlugField(max_length=64, unique=True, null=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'рубрику'
        verbose_name_plural = 'рубрики'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=32, verbose_name='тег')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='теги')
    
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments",
                             verbose_name='статья')
    name = models.CharField(max_length=64, verbose_name='комментатор')
    body = models.TextField(verbose_name='комментарий')
    email = models.EmailField(verbose_name='эл.почта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='оставлен')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    active = models.BooleanField(default=True, verbose_name='аккаунт активен')

    class Meta:
        ordering = ('created',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class Slide(models.Model):
    title = models.CharField(max_length=50, blank=True, verbose_name='заголовок')
    subtitle = models.CharField(max_length=50, blank=True, verbose_name='подзаголовок')
    text = models.CharField(max_length=50, blank=True, verbose_name='текст')
    picture = models.ImageField(upload_to='slides/', blank=True, verbose_name='слайд')
    link = models.CharField(max_length=50, blank=True, verbose_name='сссылка')

    class Meta:
        ordering = ('text',)
        verbose_name = 'слайд'
        verbose_name_plural = 'слайды'

    def __str__(self):
        return self.title


class SlideTextItem(models.Model):
    textItem = models.ForeignKey(Slide, related_name='items', on_delete=models.CASCADE, verbose_name='пункт')
    text = models.CharField(max_length=50, blank=True, verbose_name='позиция')
