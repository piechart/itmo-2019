# -*- coding: utf-8 -*-

from django.test import TestCase
from ..services import notification_service
from ..models import *

class Testnotification_service(TestCase):
    """Tests."""

    def setUp(self):
        """SetUp."""
        pizza = Pizza(id=1, title='CheesyPizza', price=10)
        pizza.save()

        order = Order()
        order.status = OrderType.COOKING
        order.save()
        order.pizzas = [pizza]

    def test_cooking_pizzas_count(self):
        """Test."""
        self.assertEqual(notification_service.cooking_pizzas_count(), 1)

    def test_delivery_time_estimation(self):
        """Test."""
        self.assertEqual(notification_service.notify_customer(hour=2), 'order will be delivered in 70 minutes')
        self.assertEqual(notification_service.notify_customer(hour=14), 'order will be delivered in 50 minutes')
