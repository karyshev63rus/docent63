from django.db import models
from django.conf import settings
from listings.models import Product
from django.shortcuts import reverse


ORDER_STATUS = [
    ('Created', 'Создан'),
    ('Paid', 'Оплачен'),
    ('Shipped', 'Отправлен получателю'),
    ('Ready for pickup', 'Готов к выдаче'),
    ('Completed', 'Завершен')
]

TRANSPORT_CHOICES = [
    ('курьером', 'курьером'),
    ('самовывоз', 'самовывоз')
]


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orders',
                             blank=True,
                             null = True, verbose_name='пользователь')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='эл.почта')
    telephone = models.CharField(max_length=20, verbose_name='телефон')
    address = models.CharField(max_length=250, verbose_name='адрес')
    postal_code = models.CharField(max_length=20, verbose_name='индекс')
    city = models.CharField(max_length=100, verbose_name='город')
    country = models.CharField(max_length=100, verbose_name='страна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлено')
    status = models.CharField(max_length=20, choices=ORDER_STATUS,
                              default='Создан', verbose_name='статус заказа')
    note = models.TextField(blank=True, verbose_name='пожелания')
    transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES,
                                 verbose_name='условия доставки')
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='стоимость доставки')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Order #{self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost += self.transport_cost
        return total_cost

    def get_absolute_url(self):
        return reverse('orders:order_detail',
                       args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,
                              verbose_name='заказ')
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE, verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='цена')
    quantity = models.PositiveIntegerField(verbose_name='количество')
    
    class Meta:
        verbose_name = 'позицию заказа'
        verbose_name_plural = 'позиции заказа'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    link = models.CharField(max_length=100, verbose_name='ссылка на оплату заказа')

    class Meta:
        verbose_name = 'ссылка на оплату'
        verbose_name_plural = 'ссылки на оплату'

    def __str__(self):
        return f'Payment Link {self.link}'
