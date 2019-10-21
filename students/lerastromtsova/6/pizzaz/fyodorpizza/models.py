# -*- coding: utf-8 -*-

from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    ingredient_list = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name


class Order(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
                              choices=[('accept', 'accept'),
                                       ('preparation', 'preparation'),
                                       ('delivery', 'delivery'),
                                       ('done', 'done'),
                                       ],
                              default='accept')
    pizza_list = models.ManyToManyField(Pizza)
    delivery_address = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=50)
    email_is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.pizza_list
