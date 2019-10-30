from main.models import *
import datetime

def cooking_pizzas_count():
    orders = Order.objects.filter(status=OrderType.COOKING)
    pizzas = map(lambda order: order.pizzas, orders)
    return len([pizza for pizza in pizzas])

def notify_customer(hour=datetime.datetime.now().hour):
    delay = 40 if (10 <= hour <= 22) else 60
    duration = cooking_pizzas_count() * 10 + delay
    return 'order will be delivered in {0} minutes'.format(duration)
