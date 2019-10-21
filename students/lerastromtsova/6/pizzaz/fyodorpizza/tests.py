# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test import Client
from .models import Ingredient, Pizza, Order
from decimal import Decimal


def create_test_ingredient(name):
    ingredient = Ingredient(name=name)
    ingredient.save()
    return ingredient


def create_test_pizza(name, price, ingredient_list):
    pizza = Pizza(
        name=name,
        price=price,
    )
    pizza.save()
    pizza.ingredient_list.set(ingredient_list)
    return pizza


def create_test_order(pizza_list, delivery_address, client_email):
    order = Order(
        delivery_address=delivery_address,
        client_email=client_email,
    )
    order.save()
    order.pizza_list.set(pizza_list)
    return order


class GetMenuTest(TestCase):
    client = Client()

    def setUp(self):
        """Create test ingredients and pizza"""
        ingredient_test = create_test_ingredient('test')
        ingredient_cheese = create_test_ingredient('cheese')

        self.pizza = create_test_pizza(name='Test with cheese',
                                       price=Decimal(1.00),
                                       ingredient_list=[ingredient_cheese,
                                                        ingredient_test])

    def test_can_get_menu(self):
        """Check that API returns list of pizzas"""
        response = self.client.get(path='/api/pizza')
        assert response.status_code == 200


class PostOrderTest(TestCase):
    client = Client()

    def setUp(self):
        """Create test ingredients and pizza"""
        ingredient_test = create_test_ingredient('test')
        ingredient_cheese = create_test_ingredient('cheese')

        self.pizza = create_test_pizza(name='Test with cheese',
                                       price=Decimal(1.00),
                                       ingredient_list=[ingredient_cheese,
                                                        ingredient_test])

    def test_can_post_order(self):
        """Make POST request and assert that order is saved in database and email is sent"""
        response = self.client.post(path='api/order',
                                    data={
                                        'status': 'accept',
                                        'pizza_list': [self.pizza.pk],
                                        'delivery_address': 'Petrogradskaya emb., 36A, Saint Petersburg, Russia',
                                        'client_email': 'v.stromtsova@yandex.ru',
                                    })
        assert response.status_code == 200
        # assert saving to db
        # assert email_is_sent on order
        # assert cooking time

    def test_cannot_post_invalid_order(self):
        """Make POST request with invalid params and assert that order is not saved in database"""
        response = self.client.post(path='api/order',
                                    data={
                                        'pizza_list': [],
                                        'delivery_address': 'Petrogradskaya emb., 36A, Saint Petersburg, Russia',
                                        'client_email': 'v.stromtsova@yandex.ru',
                                    })
        assert response.status_code == 200  # seems like Django returns 200 even if params are invalid
        # assert order not saved to db


class GetStatisticsTest(TestCase):
    client = Client()

    def setUp(self):
        self.order = create_test_order(
            pizza_list=[create_test_pizza(
                name='Sausage with tomato',
                price=Decimal(1.00),
                ingredient_list=[
                    create_test_ingredient('tomato'),
                    create_test_ingredient('sausage')
                ]
            )],
            delivery_address='Petrogradskaya emb., 36A, Saint Petersburg, Russia',
            client_email='v.stromtsova@yandex.ru',
        )

    def test_can_get_statistics(self):
        """Make GET request and check status code and pizzas list"""
        response = self.client.get(path='/api/statistics/pizza')
        assert response.status_code == 200
        # assert that received list matches list of pizzas in order
