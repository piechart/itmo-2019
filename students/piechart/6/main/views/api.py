# -*- coding: utf-8 -*-

from django.http import JsonResponse
from main.models import *
from main.services import notification_service, order_service, date_service


def get_pizzas():
    """Returns pizzas list."""
    response = {
        'pizzas': [
            pizza.as_dict() for pizza in Pizza.objects.all()  # noqa F405
        ],
    }
    return JsonResponse(response)


def create_order(request):  # noqa WPS210, WPS212
    """Creates order."""
    def resolve_pizza(pizza_title):  # noqa WPS430
        pizza = Pizza.objects.get(title=pizza_title)  # noqa F405
        if pizza is not None:
            return pizza
        return None

    address = request.POST.get('address')
    email = request.POST.get('email')

    if not address or not email:
        return JsonResponse({
            'result': 'error',
            'error': 'no address or email provided',
        })

    pizza_titles = request.POST.get('pizzas')
    if not pizza_titles:
        return JsonResponse({
            'result': 'error',
            'error': 'no pizzas provided',
        })

    pizza_titles = pizza_titles.split(',')
    pizza_items = [resolve_pizza(title) for title in pizza_titles]
    pizzas = [pizza for pizza in pizza_items if pizza is not None]
    if not pizzas:
        return JsonResponse({
            'result': 'error',
            'error': 'no valid pizzas provided',
        })

    order = Order(  # noqa F405
        place_date=date_service.date_object(date_service.today()),
        delivery_address=address,
        customer_email=email,
        status=OrderType.ACCEPTED,  # noqa F405
    )
    order.save()
    order.pizzas = pizzas

    notification_service.notify_customer()

    return JsonResponse({
        'result': 'success',
        'order_id': order.pk,
    })


def stats(request):  # noqa WPS210
    """Returns stats."""
    if 'date' in request.GET:
        date = date_service.date_object(request.GET.get('date'))
    else:
        date = date_service.today()
    orders = Order.objects.filter(place_date=date)  # noqa F405

    res = {
        'total_orders': len(orders),
        'accepted_orders': order_service.count_by_status(
            orders,
            OrderType.ACCEPTED,  # noqa F405
        ),
        'cooking_orders': order_service.count_by_status(
            orders,
            OrderType.COOKING,  # noqa F405
        ),
        'delivery_orders': order_service.count_by_status(
            orders,
            OrderType.DELIVERY,  # noqa F405
        ),
        'completed_orders': order_service.count_by_status(
            orders,
            OrderType.COMPLETED,  # noqa F405
        ),
    }

    ordered_pizza_titles = []
    for pizzas in map(lambda order: order.pizzas, orders):
        for pizza in pizzas.all():
            ordered_pizza_titles.append(pizza.title)

    res['ordered_pizzas'] = [
        {
            'pizza_title': title,
            'count': ordered_pizza_titles.count(title),
        } for title in ordered_pizza_titles
    ]

    return JsonResponse(res)
