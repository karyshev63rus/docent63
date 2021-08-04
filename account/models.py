from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, verbose_name='пользователь')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='телефон')
    address = models.CharField(max_length=250, blank=True, verbose_name='адрес')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='индекс')
    city = models.CharField(max_length=100, blank=True, verbose_name='город')
    country = models.CharField(max_length=100, blank=True, verbose_name='страна')

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return f'{self.user.username} profile'
