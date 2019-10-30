# -*- coding: utf-8 -*-

import datetime

from main.models import *  # noqa F403


def cooking_pizzas_count():
    """Counts pizzas from orders which status is COOKING."""
    orders = Order.objects.filter(status=OrderType.COOKING)  # noqa F405
    pizzas = map(lambda order: order.pizzas, orders)
    return len([pizza for pizza in pizzas])


def notify_customer(hour=datetime.datetime.now().hour):  # noqa WPS404
    """Fake email sending function."""
    delay = 40 if (10 <= hour <= 22) else 60  # noqa WPS432
    duration = cooking_pizzas_count() * 10 + delay
    return 'order will be delivered in {0} minutes'.format(duration)
