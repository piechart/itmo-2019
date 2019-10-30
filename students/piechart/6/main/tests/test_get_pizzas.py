# -*- coding: utf-8 -*-

from django.test import TestCase

from ..views import api

from ..tests import shared_tests_logic

class TestGetPizzas(TestCase):
    """Tests."""

    def decode_json(self, json_response):
        """Decodes json."""
        return json_response._container[0].decode('utf-8')

    def test_no_pizzas(self):
        """Test."""
        self.assertEqual(self.decode_json(api.get_pizzas()), '{"pizzas": []}')

    def test_get_pizzas(self):
        """Test."""
        shared_tests_logic.make_test_data()
        self.assertEqual(self.decode_json(api.get_pizzas()), '{"pizzas": [{"id": 1, "title": "CheesyPizza", "price": 10, "ingredients": [{"id": 1, "title": "Cheese"}]}]}')
