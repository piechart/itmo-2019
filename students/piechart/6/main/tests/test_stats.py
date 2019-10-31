# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase

from main.models import Order, OrderType
from main.tests import shared_tests_logic
from main.views import api


class TestStats(TestCase):
    """Tests."""

    def decode_json(self, json_response):
        """Decode."""
        return json_response._container[0].decode('utf-8')  # noqa WPS437

    def test_empty_stats(self):
        """Test."""
        res = api.stats(HttpRequest())
        assert self.decode_json(res) == '{0}{1}{2}'.format(
            '{"total_orders": 0, "accepted_orders": 0, ',
            '"cooking_orders": 0, "delivery_orders": 0, ',
            '"completed_orders": 0, "ordered_pizzas": []}',
        )

    def test_accepted_stats(self):
        """Test."""
        pizza = shared_tests_logic.make_test_data()

        order = Order(
            delivery_address='address',
            customer_email='e@ma.il',
            status=OrderType.ACCEPTED,
        )
        order.save()
        order.pizzas.set([pizza])

        res = api.stats(HttpRequest())
        assert self.decode_json(res) == '{0}{1}{2}{3}'.format(
            '{"total_orders": 1, "accepted_orders": 1, "cooking_orders',
            '": 0, "delivery_orders": 0, "completed_orders": ',
            '0, "ordered_pizzas": [{"pizza_title":',
            ' "CheesyPizza", "count": 1}]}',
        )
