from django.conf import settings
import requests


def sent_telegram_messages(order_id, first_name, last_name, telephone, email, total_cost):
    tg_token = settings.TG_TOKEN
    tg_chat_id = settings.TG_CHAT_ID
    api = 'https://api.telegram.org/bot'
    method = api + tg_token + '/sendMessage'
    requests.post(method, data={
            'chat_id': tg_chat_id,
            'text': f'Оформлен заказ № {order_id}\n'
                    f'на сумму {total_cost} д.е.\n'
                    f'Покупатель: {first_name} {last_name}\n'
                    f'тел.: {telephone}\n'
                    f'эл.почта: {email}'
    })
