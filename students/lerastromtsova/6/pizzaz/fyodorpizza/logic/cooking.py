# -*- coding: utf-8 -*-

from fyodorpizza.models import Order

MINUTES_PER_PIZZA = 10
COOK_IN_WORK_HRS = 40
COOK_OUT_WORK_HRS = 60


def count_cooking_time(creation_date):
    """Counts time depending on order date & number of pizzas cooking."""
    cooking_left = get_number_of_pizzas_state() * MINUTES_PER_PIZZA
    during_work_hours = is_order_during_work_hours(creation_date)
    cooking_this = COOK_IN_WORK_HRS if during_work_hours else COOK_OUT_WORK_HRS
    return cooking_left + cooking_this


def get_number_of_pizzas_state(state='cooking'):
    """Gets number of pizzas in any state, default 'cooking'."""
    orders = Order.objects.filter(status=state)
    return sum(order.pizza_list.count() for order in orders)


def is_order_during_work_hours(order_time, work_hours=(10, 22)):
    """Defines if the order is made during work hours."""
    hour = order_time.hour
    if work_hours[0] <= hour < work_hours[1]:
        return True
    return False
