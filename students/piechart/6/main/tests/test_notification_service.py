# -*- coding: utf-8 -*-

from django.test import TestCase

from main.models import Order, OrderType, Pizza
from main.services import notification_service


class TestNotificationService(TestCase):
    """Tests."""

    def setUp(self):
        """SetUp."""
        Order.objects.filter(status=OrderType.COOKING).delete()

        pizza = Pizza(id=1, title='CheesyPizza', price=10)
        pizza.save()

        order = Order()
        order.status = OrderType.COOKING
        order.save()
        order.pizzas.set([pizza])

    def test_cooking_pizzas_count(self):
        """Test."""
        assert notification_service.cooking_pizzas_count() == 1

    def test_delivery_time_estimation(self):
        """Test."""
        delivery70 = 'order will be delivered in 70 minutes'
        r1 = notification_service.notify_customer(hour=2)
        assert r1 == delivery70
        delivery50 = 'order will be delivered in 50 minutes'
        hours = 14
        r2 = notification_service.notify_customer(hour=hours)
        assert r2 == delivery50
