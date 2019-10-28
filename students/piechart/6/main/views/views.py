# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
# from main.forms import *

def cabinet(request):
    return render(request, "cabinet.html")

