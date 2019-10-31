# -*- coding: utf-8 -*-

from django.db import models

letter_s = 'S'
letter_m = 'M'  # I do this stupid thing because of flake8
letter_l = 'L'

sizes = {
    letter_s: 20,
    letter_m: 50,
    letter_l: 100,
}
SIZES = frozenset(sizes.items())

PRICE_DECIMAL_PLACES = 2
PRICE_MAX_DIGITS = 8


class Ingredient(models.Model):
    """A model that describes :term:`Ingredient` object."""

    name = models.CharField(max_length=dict(SIZES)[letter_m], unique=True)

    def __str__(self):
        """Returns string representation of :term:`Ingredient`."""
        return self.name


class Pizza(models.Model):
    """A model that describes :term:`Pizza` object."""

    name = models.CharField(max_length=dict(SIZES)[letter_m], unique=True)
    price = models.DecimalField(
        decimal_places=PRICE_DECIMAL_PLACES,
        max_digits=PRICE_MAX_DIGITS,
    )
    ingredient_list = models.ManyToManyField(Ingredient)

    def __str__(self):
        """Returns string representation of :term:`Pizza`."""
        return self.name


class Order(models.Model):
    """A model that describes :term:`Order` object."""

    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=dict(SIZES)[letter_s],
        choices=[
            ('accept', 'accept'),
            ('preparation', 'preparation'),
            ('delivery', 'delivery'),
            ('done', 'done'),
        ],
        default='accept',
    )
    pizza_list = models.ManyToManyField(Pizza)
    delivery_address = models.CharField(max_length=dict(SIZES)[letter_l])
    client_email = models.EmailField(max_length=dict(SIZES)[letter_m])
    email_is_sent = models.BooleanField(default=False)

    def __str__(self):
        """Returns string representation of :term:`Order`."""
        return 'Created: {0}, status: {1}'.format(
            self.creation_date,
            self.status,
        )
