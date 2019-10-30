from django.test import TestCase
from ..services import NotificationService
from ..models import *

class TestNotificationService(TestCase):

    def setUp(self):
        pizza = Pizza(id=1, title='CheesyPizza', price=10)
        pizza.save()

        order = Order()
        order.status = OrderType.COOKING
        order.save()
        order.pizzas = [pizza]

    def test_cooking_pizzas_count(self):
        self.assertEqual(NotificationService.cooking_pizzas_count(), 1)

    def test_delivery_time_estimation(self):
        self.assertEqual(NotificationService.notify_customer(hour=2), 'order will be delivered in 70 minutes')
        self.assertEqual(NotificationService.notify_customer(hour=14), 'order will be delivered in 50 minutes')
