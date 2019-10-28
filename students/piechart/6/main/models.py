# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
from enum import Enum

class OrderType(Enum):
    ACCEPTED = "ACCEPTED"
    COOKING = "COOKING"
    DELIVERY = "DELIVERY"
    COMPLETED = "COMPLETED"
    
    def __str__(self):
        return self.value

class Ingredient(models.Model):
    title = models.CharField(max_length=64)
    
    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title
        }

class Pizza(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)
    
    def as_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "price": self.price,
            "ingredients": [ingredient.as_dict() for ingredient in self.ingredients]
        }
        
class Order(models.Model):
    place_date = models.DateField(default=date.today)
    pizzas = models.ManyToManyField(Pizza)
    delivery_address = models.CharField(max_length=128)
    customer_email = models.CharField(max_length=64)
    status = models.CharField(
        max_length=4,
        choices=[(st, st.value) for st in OrderType]
    )
    
    def as_dict(self):
        return {
            "place_date": self.place_date,
            "pizzas": [pizza.as_dict() for pizza in self.pizzas],
            "delivery_address": self.delivery_address,
            "customer_email": self.customer_email,
            "status": str(self.status[1])
        }
    
    
    
    
    
    
    