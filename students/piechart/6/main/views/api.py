# -*- coding: utf-8 -*-

from django.http import JsonResponse  # noqa I003
from typing import Dict, Any  # noqa I001

from main.models import Order, OrderType, Pizza
from main.services import date_service, notification_service, order_service

RESULT = 'result'
ERROR = 'error'

# type: ignore  # noqa E800


def get_pizzas(request) -> JsonResponse:
    """Returns pizzas list."""
    response = {
        'pizzas': [
            pizza.as_dict() for pizza in Pizza.objects.all()
        ],
    }
    return JsonResponse(response)


def create_order(request) -> JsonResponse:  # noqa WPS210, WPS212
    """Creates order."""
    def resolve_pizza(pizza_title) -> Pizza:  # noqa WPS430
        return Pizza.objects.get(title=pizza_title)

    address = request.POST.get('address')
    email = request.POST.get('email')

    if not address or not email:
        return JsonResponse({
            RESULT: ERROR,
            ERROR: 'no address or email provided',
        })

    pizza_titles = request.POST.get('pizzas')
    if not pizza_titles:
        return JsonResponse({
            RESULT: ERROR,
            ERROR: 'no pizzas provided',
        })

    pizza_titles = pizza_titles.split(',')
    pizza_items = [resolve_pizza(title) for title in pizza_titles]
    pizzas = [pizza for pizza in pizza_items]
    if len(pizzas) == 0:  # noqa WPS507
        return JsonResponse({
            RESULT: ERROR,
            ERROR: 'no valid pizzas provided',
        })

    order = Order(
        place_date=date_service.date_object(date_service.today()),
        delivery_address=address,
        customer_email=email,
        status=OrderType.ACCEPTED,
    )
    order.save()
    order.pizzas.set(pizzas)

    notification_service.notify_customer()

    return JsonResponse({
        RESULT: 'success',
        'order_id': order.pk,
    })


def stats(request) -> JsonResponse:  # noqa WPS210
    """Returns stats."""
    if 'date' in request.GET:
        date = request.GET.get('date')
    else:
        date = date_service.today()
    orders = Order.objects.filter(place_date=date)

    res: Dict[str, Any] = {
        'total_orders': len(orders),
        'accepted_orders': order_service.count_by_status(
            orders,
            OrderType.ACCEPTED,
        ),
        'cooking_orders': order_service.count_by_status(
            orders,
            OrderType.COOKING,
        ),
        'delivery_orders': order_service.count_by_status(
            orders,
            OrderType.DELIVERY,
        ),
        'completed_orders': order_service.count_by_status(
            orders,
            OrderType.COMPLETED,
        ),
    }

    ordered_pizza_titles = []
    for pizzas in map(lambda order: order.pizzas, orders):
        for pizza in pizzas.all():
            ordered_pizza_titles.append(pizza.title)

    ordered_pizzas = []
    for title in ordered_pizza_titles:
        pizza_obj = {
            'pizza_title': title,
            'count': ordered_pizza_titles.count(title),
        }
        ordered_pizzas.append(pizza_obj)
    res['ordered_pizzas'] = ordered_pizzas

    return JsonResponse(res)
