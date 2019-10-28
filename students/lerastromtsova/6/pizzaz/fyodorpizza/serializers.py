# -*- coding: utf-8 -*-

from fyodorpizza import models
from rest_framework import serializers


class PizzaSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Pizza` objects."""

    class Meta(object):
        """Serializer setup."""

        model = models.Pizza
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Ingredient` objects."""

    class Meta(object):
        """Serializer setup."""

        model = models.Ingredient
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """A class for serializing :term:`Order` objects."""

    class Meta(object):
        """Serializer setup."""

        model = models.Order
        fields = '__all__'
