# -*- coding: utf-8 -*-

from datetime import date
from enum import Enum

from django.db import models


class OrderType(Enum):
    """Useful class313."""

    ACCEPTED = 'ACCEPTED'  # noqa WPS115
    COOKING = 'COOKING'  # noqa WPS115
    DELIVERY = 'DELIVERY'  # noqa WPS115
    COMPLETED = 'COMPLETED'  # noqa WPS115

    def __str__(self):
        """Useful func1."""
        return self.value


class Ingredient(models.Model):
    """Useful class2."""

    ml1 = 64
    title = models.CharField(max_length=ml1)

    def as_dict(self):
        """Useful func12."""
        return {
            'id': self.pk,
            'title': self.title,
        }


class Pizza(models.Model):
    """Useful class312."""

    m1 = 64
    title = models.CharField(max_length=m1)
    price = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)

    def as_dict(self):
        """Useful func2314."""
        ingredients = self.ingredients.all()
        return {
            'id': self.pk,
            'title': self.title,
            'price': self.price,
            'ingredients': [
                ingredient.as_dict() for ingredient in ingredients
            ],
        }


class Order(models.Model):
    """Useful class1344."""

    place_date = models.DateField(default=date.today)
    pizzas = models.ManyToManyField(Pizza)
    m1 = 126
    m2 = 64
    delivery_address = models.CharField(max_length=m1)
    customer_email = models.CharField(max_length=m2)
    m3 = 16
    status = models.CharField(
        max_length=m3,
        choices=[
            (ord_type.value, ord_type.value) for ord_type in OrderType
        ],
    )

    def as_dict(self):
        """Useful func1431."""
        pizzas = self.pizzas.all()
        return {
            'id': self.pk,
            'place_date': self.place_date,
            'pizzas': [
                pizza.as_dict() for pizza in pizzas
            ],
            'delivery_address': self.delivery_address,
            'customer_email': self.customer_email,
            'status': str(self.status[1]),
        }
