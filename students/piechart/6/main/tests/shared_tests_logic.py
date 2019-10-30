from ..models import *

def make_test_data():
    cheese = Ingredient(title='Cheese')
    cheese.save()

    pizza = Pizza(id=1, title='CheesyPizza', price=10)
    pizza.save()

    pizza.ingredients = [cheese]

    return pizza
