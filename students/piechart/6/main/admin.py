# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import *

admin.site.register(Ingredient)
admin.site.register(Pizza)
admin.site.register(Order)