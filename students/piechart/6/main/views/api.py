import json

from django.http import JsonResponse
from main.models import *
import datetime

def get_pizzas(request):
    response = {
        "pizzas": [pizza.as_dict() for pizza in Pizza.objects.all()]
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

    pizza_titles = request.POST.get('pizzas').split(',')
    pizza_items = map(lambda title: resolve_pizza(title), pizza_titles)
    pizzas = [pizza for pizza in pizza_items if pizza is not None]
    if not pizzas:
        return JsonResponse({
            "result": "error",
            "error": "no valid pizzas provided"
        })

    order = Order(
        place_date=datetime.strptime(today(), '%Y-%m-%d'),
        pizzas=pizzas,
        delivery_address=address,
        customer_email=email,
        status=OrderType.ACCEPTED
    )
    order.save()

    notify_customer(email)

    return JsonResponse({
        "result": "success",
        "order_id": order.pk
    })

def stats(request):
    orders = Order.objects.filter(place_date=today())

    response = {
        'total_orders': len(orders)
    }
    response['accepted_orders'] = filter_by_status(orders, OrderType.ACCEPTED)
    response['cooking_orders'] = filter_by_status(orders, OrderType.COOKING)
    response['delivery_orders'] = filter_by_status(orders, OrderType.DELIVERY)
    response['completed_orders'] = filter_by_status(orders, OrderType.COMPLETED)

    ordered_pizza_titles_flat = map(lambda order: order.pizzas, orders)
    ordered_pizza_titles = []
    for pizzas in ordered_pizza_titles_flat:
        for pizza in pizzas.all():
            ordered_pizza_titles.append(pizza.title)

    ordered_pizzas = []
    for title in ordered_pizza_titles:
        ordered_pizzas.append({'pizza_title': title, 'count': ordered_pizza_titles.count(title)})
    response['ordered_pizzas'] = ordered_pizzas

    return JsonResponse(response)

def filter_by_status(orders, status):
    return len(list(filter(lambda order: str(order.status) == str(status), orders)))

def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def notify_customer():
    orders = Order.objects.filter(status=OrderType.COOKING)
    pizzas = map(lambda order: order.pizzas, orders)
    count = len([pizza for pizza in pizzas])
    hour = datetime.datetime.now().hour
    duration = count * 10 + 40 if (hour >= 10 and hour <= 22) else 60
    return 'delivery after {0} minutes'.format(duration)
