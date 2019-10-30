# -*- coding: utf-8 -*-

from django.core.mail import send_mail

from fyodorpizza.logic.cooking import count_cooking_time
from fyodorpizza.models import Order


def send_mail_on_order(order: Order):
    """Sends mail concerning any order."""
    send_mail(
        'Your pizza is on the way!',
        'It will arrive in {0}'.format(count_cooking_time(order.creation_date)),
        'test-stromtsova@yandex.ru',
        [order.client_email],
        fail_silently=False,
    )
    order.email_is_sent = True
    order.save()
    return order
