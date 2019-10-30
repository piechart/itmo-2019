from django.test import TestCase
from django.http import HttpRequest

from ..models import *
from ..views import api

class TestCreateOrder(TestCase):

    def setUp(self):
        cheese = Ingredient(title='Cheese')
        cheese.save()

        pizza = Pizza(id=1, title='CheesyPizza', price=10)
        pizza.save()

        pizza.ingredients = [cheese]

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
