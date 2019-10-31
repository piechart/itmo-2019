# -*- coding: utf-8 -*-

from django.test import TestCase

from main.tests import shared_tests_logic
from main.views import api
from main.models import Pizza, Order, Ingredient  # noqa I001


class TestGetPizzas(TestCase):
    """Tests."""

    def setUp(self):
        """Setup."""
        Pizza.objects.all().delete()
        Order.objects.all().delete()
        Ingredient.objects.all().delete()

    def decode_json(self, json_response) -> str:
        """Decodes json."""
        return json_response._container[0].decode('utf-8')  # noqa WPS437

    def test_no_pizzas(self):
        """Test."""
        decode_result = self.decode_json(api.get_pizzas(None))
        assert decode_result == '{"pizzas": []}'

    def test_get_pizzas(self):
        """Test."""
        shared_tests_logic.make_test_data()
        decode_result = self.decode_json(api.get_pizzas(None))
        assert decode_result == '{0}{1}{2}'.format(
            '{"pizzas": [{"id": 1, "title": "CheesyPizza", ',
            '"price": 10, "ingredients": [{"id": 1, ',
            '"title": "Cheese"}]}]}',
        )
