from django.conf import settings
from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from io import BytesIO
import weasyprint
from .models import Order
from .telebotmsg import sent_telegram_messages


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order_id}'
    message = f'Уважаемый(ая) {order.first_name}, \n\n' \
              f'Ваш заказ успешно создан.\n' \
              f'Номер вашего заказа {order.id}.'
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.email]
    )
    html = render_to_string('pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()
    sent_telegram_messages(order_id=order.id, first_name=order.first_name,
                           last_name=order.last_name, telephone=order.telephone,
                           email=order.email, total_cost=order.get_total_cost())


@task
def status_change_notification(order_id):
    order = Order.objects.get(id=order_id)
    print(order)
    subject = f'Заказ #{order_id}'
    message = f'Уважаемый(ая) {order.first_name}, \n\n' \
              f'Статус вашего заказа #{order.id} изменен на "{order.status}".'
    mail_sent = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.email]
    )
    return mail_sent
