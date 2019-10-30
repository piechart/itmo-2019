from django.test import TestCase
from django.http import HttpRequest

from ..models import *
from ..views import api

from ..tests import shared_tests_logic

class TestStats(TestCase):

    def decode_json(self, json_response):
        return json_response._container[0].decode('utf-8')

    def test_empty_stats(self):
        res = api.stats(HttpRequest())
        self.assertEqual(self.decode_json(res), '{"total_orders": 0, "accepted_orders": 0, "cooking_orders": 0, "delivery_orders": 0, "completed_orders": 0, "ordered_pizzas": []}')

    def test_accepted_stats(self):
        pizza = shared_tests_logic.make_test_data()
        
        order = Order(
            delivery_address='address',
            customer_email='e@ma.il',
            status=OrderType.ACCEPTED
        )
        order.save()
        order.pizzas = [pizza]

        res = api.stats(HttpRequest())
        self.assertEqual(self.decode_json(res), '{"total_orders": 1, "accepted_orders": 1, "cooking_orders": 0, "delivery_orders": 0, "completed_orders": 0, "ordered_pizzas": [{"pizza_title": "CheesyPizza", "count": 1}]}')
