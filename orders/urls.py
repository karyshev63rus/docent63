from django.urls import path
from . import views, payment
from django.contrib.admin.views.decorators import staff_member_required
from config.decorators import user_created_order


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/pdf/', staff_member_required(views.invoice_pdf),
                                        name='invoice_pdf'),
    path('order/<int:order_id>/pdf/', user_created_order(views.invoice_pdf),
                                        name='customer_invoice_pdf'),
    path('order/<int:order_id>/', user_created_order(views.order_detail), name='order_detail'),
    path('order/pay/<int:order_id>/', payment.order_pay, name='order_pay'),
    path('order/pay/link/<int:order_id>/', payment.order_pay_link, name='order_pay_link'),
    path('order/pay/confirm/<int:order_id>/', payment.order_pay_confirm, name='order_pay_confirm'),
    path('api/', payment.PaymentLinkAPIView.as_view(), name='payment_link_apy'),
]
