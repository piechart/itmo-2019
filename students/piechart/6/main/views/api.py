import json

from django.http import JsonResponse
from main.models import *
from main.services import NotificationService, OrderService, DateService
import datetime

def get_pizzas():
    response = {
        'pizzas': [pizza.as_dict() for pizza in Pizza.objects.all()]
    }
    return JsonResponse(response)

def create_order(request):
    def resolve_pizza(pizza_title):
        pizza = Pizza.objects.get(title=pizza_title)
        if pizza is not None:
            return pizza
        return None

    address = request.POST.get('address')
    email = request.POST.get('email')

    if not address or not email:
        return JsonResponse({
            'result': 'error',
            'error': 'no address or email provided'
        })

    pizza_titles = request.POST.get('pizzas')
    if not pizza_titles:
        return JsonResponse({
            'result': 'error',
            'error': 'no pizzas provided'
        })

    pizza_titles = pizza_titles.split(',')
    pizza_items = map(lambda title: resolve_pizza(title), pizza_titles)
    pizzas = [pizza for pizza in pizza_items if pizza is not None]
    if not pizzas:
        return JsonResponse({
            'result': 'error',
            'error': 'no valid pizzas provided'
        })

    order = Order(
        place_date=DateService.date_object(DateService.today()),
        delivery_address=address,
        customer_email=email,
        status=OrderType.ACCEPTED
    )
    order.save()
    order.pizzas = pizzas

    NotificationService.notify_customer()

    return JsonResponse({
        'result': 'success',
        'order_id': order.pk
    })

def stats(request):
    if 'date' in request.GET:
        date = DateService.date_object(request.GET.get('date'))
    else:
        date = DateService.today()
    orders = Order.objects.filter(place_date=date)

    res = {
        'total_orders': len(orders),
        'accepted_orders': OrderService.count_by_status(orders, OrderType.ACCEPTED),
        'cooking_orders': OrderService.count_by_status(orders, OrderType.COOKING),
        'delivery_orders': OrderService.count_by_status(orders, OrderType.DELIVERY),
        'completed_orders': OrderService.count_by_status(orders, OrderType.COMPLETED)
    }

    pizza_titles_flattened = map(lambda order: order.pizzas, orders)
    ordered_pizza_titles = []
    for pizzas in pizza_titles_flattened:
        for pizza in pizzas.all():
            ordered_pizza_titles.append(pizza.title)

    res['ordered_pizzas'] = [
        {
            'pizza_title': title,
            'count': ordered_pizza_titles.count(title)
        }
            for title in ordered_pizza_titles
    ]

    return JsonResponse(res)
