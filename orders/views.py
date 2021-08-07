from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Product
from .forms import OrderCreateForm
from cart.views import get_cart, cart_clear
from decimal import Decimal
from .tasks import order_created, status_change_notification
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

TRANSPORT_BASE_COST = 3.99
TRANSPORT_EXTRA_COST_RATE = 1.5


def order_create(request):
    cart = get_cart(request)
    transport_cost = get_transport_cost(request, cart)
    if request.method == 'POST':
        order = save_valid_order_form(request, transport_cost)
        create_order_items_list(cart, order)
        cart_clear(request)
        order_created.delay(order.id)
        return redirect('orders:order_pay', order.id)
    order_form = get_order_form(request)
    return render(request,
                  'order_create.html',
                  {'cart': cart,
                   'order_form': order_form,
                   'transport_cost': transport_cost})


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


def get_transport_cost(request, cart):
    cart_qty = sum(item['quantity'] for item in cart.values())
    transport_cost = str(round((TRANSPORT_BASE_COST + (cart_qty // 10) * TRANSPORT_EXTRA_COST_RATE), 2))
    return transport_cost


def save_valid_order_form(request, transport_cost):
    order_form = OrderCreateForm(request.POST)
    if order_form.is_valid():
        cf = order_form.cleaned_data
        transport = cf['transport']
        if transport == 'самовывоз':
            transport_cost = 0
    order = order_form.save(commit=False)
    if request.user.is_authenticated:
        order.user = request.user
    order.transport_cost = Decimal(transport_cost)
    order.save()
    return order


def create_order_items_list(cart, order):
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    for product in products:
        cart_item = cart[str(product.id)]
        OrderItem.objects.create(
            order=order,
            product=product,
            price=cart_item['price'],
            quantity=cart_item['quantity']
        )


def get_order_form(request):
    order_form = OrderCreateForm()
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'telephone': request.user.profile.phone_number,
            'address': request.user.profile.address,
            'postal_code': request.user.profile.postal_code,
            'city': request.user.profile.city,
            'country': request.user.profile.country,
        }
        order_form = OrderCreateForm(initial=initial_data)
    return order_form


def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    html = render_to_string('pdf.html', {'order': order})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response


def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_detail.html',
                  {'order': order})
