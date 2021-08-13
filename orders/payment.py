import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Order, Payment
from .tasks import status_change_notification
from rest_framework import generics, serializers

PAYMENT_URL = settings.PAYMENT_URL


def order_pay_link(request, order_id):
    order = Order.objects.get(id=order_id)
    data = {'payment_system_token': settings.PS_TOKEN,
            'order_id': order.id,
            'order_total_cost': order.get_total_cost,
            'link_for_back_redirect_to_shop':
                f'https://docent63.ru/orders/order/pay/confirm/{order_id}/'}
    response = requests.get(PAYMENT_URL, data)
    link = response.json()[0]['link']
    order_pay_link_url = f'{link}{order_id}'
    return HttpResponseRedirect(order_pay_link_url)


def order_pay(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request,
                  'order_pay.html',
                  {'order': order})


def order_pay_confirm(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Оплачен'
    order.save(update_fields=['status'])
    status_change_notification.delay(order_id=order.id)
    return render(request, 'order_created.html', {'order': order})


class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'link')


class PaymentLinkAPIView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentLinkSerializer
