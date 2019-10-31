# -*- coding: utf-8 -*-

from django.contrib import admin

from main.models import Ingredient, Order, Pizza

admin.site.register(Ingredient)
admin.site.register(Pizza)
admin.site.register(Order)
