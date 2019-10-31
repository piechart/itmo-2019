# -*- coding: utf-8 -*-

from django.http import HttpRequest
from django.test import TestCase

from main.tests import shared_tests_logic
from main.views import api
from main.models import Order  # noqa I001


class TestCreateOrder(TestCase):
    """Tests."""

    def setUp(self):
        """SetUp."""
        Order.objects.all().delete()
        shared_tests_logic.make_test_data()

    def decode_json(self, json_response) -> str:
        """Decode."""
        return json_response._container[0].decode('utf-8')  # noqa WPS437

    def test_create_order_no_data(self):
        """Test."""
        res = api.create_order(HttpRequest())

        valid_result = '{0}{1}'.format(
            '{"result": "error", ',
            '"error": "no address or email provided"}',
        )
        assert self.decode_json(res) == valid_result

    def test_create_order_no_pizza(self):
        """Test."""
        req = HttpRequest()
        req.POST = {
            'address': 'address',
            'email': 'email',
        }
        res = api.create_order(req)
        valid_result = '{0}{1}'.format(
            '{"result": "error", ',
            '"error": "no pizzas provided"}',
        )
        assert self.decode_json(res) == valid_result

    def test_create_order_successful(self):
        """Test."""
        req = HttpRequest()
        req.POST = {
            'address': 'address',
            'email': 'e@ma.il',
            'pizzas': 'CheesyPizza',
        }
        res = api.create_order(req)
        req_res = self.decode_json(res)
        assert 'success' in req_res
        assert 'order_id' in req_res
