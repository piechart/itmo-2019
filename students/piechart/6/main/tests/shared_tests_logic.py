# -*- coding: utf-8 -*-

from main.models import Ingredient, Pizza


def make_test_data() -> Pizza:
    """Creates test ingredient and pizza."""
    cheese = Ingredient(id=1, title='Cheese')
    cheese.save()

    pizza = Pizza(id=1, title='CheesyPizza', price=10)
    pizza.save()

    pizza.ingredients.set([cheese])

    return pizza
