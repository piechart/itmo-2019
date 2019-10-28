# -*- coding: utf-8 -*-

import json
from decimal import Decimal
from random import randint

from django.test import Client, TestCase

from fyodorpizza.models import Ingredient, Order, Pizza
from fyodorpizza.response_codes import BAD_REQUEST, CREATED, OK
from fyodorpizza.usecases.get_menu import GetMenu

TEST_ADDRESS = 'Petrogradskaya emb., 36A, SPb, Russia'
TEST_EMAIL = 'v.stromtsova@yandex.ru'

TEST_PRICE = 1
TEST_PRICE_DEC = Decimal(TEST_PRICE)


def create_test_ingredient(name):
    """Creates :term:`Ingredient` object for test purposes."""
    ingredient = Ingredient(name=name)
    ingredient.save()
    return ingredient


def create_test_pizza(name, price, ingredient_list):
    """Creates :term:`Pizza` object for test purposes."""
    pizza = Pizza(
        name=name,
        price=price,
    )
    pizza.save()
    pizza.ingredient_list.set(ingredient_list)
    return pizza


def create_test_order(pizza_list, delivery_address, client_email):
    """Creates :term:`Order` object for test purposes."""
    order = Order(
        delivery_address=delivery_address,
        client_email=client_email,
    )
    order.save()
    order.pizza_list.set(pizza_list)
    return order


class GetMenuTest(TestCase):
    """Test get_menu usecase."""

    client = Client()

    def setUp(self):
        """Create 2 test :term:`Ingredient` and :term:`Pizza`."""
        ingredient_test = create_test_ingredient('test')
        ingredient_cheese = create_test_ingredient('cheese')

        self.pizza = create_test_pizza(
            name='Test with cheese',
            price=TEST_PRICE_DEC,
            ingredient_list=[
                ingredient_cheese,
                ingredient_test,
            ],
        )

    def test_can_get_menu(self):
        """Check that API returns list of :term:`Pizza`."""
        response = self.client.get(path='/api/pizza/')
        assert response.status_code == OK

        ser_data = json.dumps(GetMenu()())
        resp_data = response.content.decode()
        assert ser_data == resp_data


class PostOrderTest(TestCase):
    """Tests post_order usecase."""

    client = Client()

    def setUp(self):
        """Create 2 test :term:`Ingredient` and :term:`Pizza`."""
        ingredient_test = create_test_ingredient('test')
        ingredient_cheese = create_test_ingredient('cheese')

        self.pizza = create_test_pizza(
            name='Test with cheese',
            price=TEST_PRICE_DEC,
            ingredient_list=[
                ingredient_cheese,
                ingredient_test,
            ],
        )

    def test_can_post_order(self):
        """Make POST request and assert status code 201 and email is sent."""
        response = self.client.post(
            path='/api/order/',
            data={
                'status': 'accept',
                'pizza_list': [self.pizza.pk],
                'delivery_address': TEST_ADDRESS,
                'client_email': TEST_EMAIL,
            },
        )
        assert response.status_code == CREATED

        # assert saving to db
        resp_data = json.loads(response.content.decode())
        order = Order.objects.get(pk=resp_data['id'])
        assert order

        # assert email_is_sent on order
        assert order.email_is_sent

    def test_cannot_post_invalid_order(self):
        """Make POST request with invalid params and assert status code 401."""
        response = self.client.post(
            path='/api/order/',
            data={
                'pizza_list': [],
                'delivery_address': TEST_ADDRESS,
                'client_email': TEST_EMAIL,
            },
        )

        assert response.status_code == BAD_REQUEST


class GetStatisticsTest(TestCase):
    """Tests get_statistics usecase."""

    client = Client()
    # random is ok for tests i think
    order_num = randint(1, 10)  # noqa: S311

    def setUp(self):
        """Make test :term:`Order`."""
        tomato = create_test_ingredient('tomato')
        sausage = create_test_ingredient('sausage')
        for onum in range(self.order_num):
            create_test_order(
                pizza_list=[
                    create_test_pizza(
                        name=str(onum),
                        price=TEST_PRICE_DEC,
                        ingredient_list=[
                            tomato,
                            sausage,
                        ],
                    ),
                ],
                delivery_address=TEST_ADDRESS,
                client_email=TEST_EMAIL,
            )

    def test_can_get_statistics(self):
        """Make GET request and check status code and :term:`Pizza` list."""
        response = self.client.get(path='/api/statistics/pizza/')

        assert response.status_code == OK

        # assert that received list matches list of pizzas in order
        resp_data = json.loads(response.content.decode())
        expected = {
            'all': self.order_num,
            'by_status': {
                'accept': self.order_num,
                'preparation': 0,
                'delivery': 0,
                'done': 0,
            },
            'by_pizza': {
                str(onum + 1): 1 for onum in range(self.order_num)
            },
        }

        assert resp_data == expected
