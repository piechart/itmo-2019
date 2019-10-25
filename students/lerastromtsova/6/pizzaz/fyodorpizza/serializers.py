# -*- coding: utf-8 -*-

from rest_framework import serializers

from fyodorpizza.models import Ingredient, Order, Pizza


class PizzaSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Pizza` objects."""

    class Meta(object):
        """Serializer setup."""

        model = Pizza
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Ingredient` objects."""

    class Meta(object):
        """Serializer setup."""

        model = Ingredient
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Order` objects."""

    class Meta(object):
        """Serializer setup."""

        model = Order
        fields = '__all__'
