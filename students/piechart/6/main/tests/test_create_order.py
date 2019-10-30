from django.test import TestCase
from django.http import HttpRequest

from ..models import *
from ..views import api

from ..tests import shared_tests_logic

class TestCreateOrder(TestCase):

    def setUp(self):
        shared_tests_logic.make_test_data()

    def decode_json(self, json_response):
        return json_response._container[0].decode('utf-8')

    def test_create_order_no_data(self):
        res = api.create_order(HttpRequest())
        self.assertEqual(self.decode_json(res), '{"result": "error", "error": "no address or email provided"}')

    def test_create_order_no_pizza(self):
        req = HttpRequest()
        req.POST = {
            'address': 'address',
            'email': 'email'
        }
        res = api.create_order(req)
        self.assertEqual(self.decode_json(res), '{"result": "error", "error": "no pizzas provided"}')

    def test_create_order_successful(self):
        req = HttpRequest()
        req.POST = {
            'address': 'address',
            'email': 'e@ma.il',
            'pizzas': 'CheesyPizza'
        }
        res = api.create_order(req)
        self.assertEqual(self.decode_json(res), '{"result": "success", "order_id": 1}')
