from django.db import models
from django.urls import reverse


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='секция')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='слаг')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'секцию'
        verbose_name_plural = 'секции'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('listings:product_list_by_section', args=[self.slug])


class Product(models.Model):
    section = models.ForeignKey(Section, related_name='products', 
                                on_delete=models.CASCADE, verbose_name='секция')
    name = models.CharField(max_length=100, unique=True, verbose_name='наименование')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='слаг')
    image = models.ImageField(upload_to='products/', verbose_name='фото')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='в наличии')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('listings:product_detail', args=[self.section.slug, self.slug])
