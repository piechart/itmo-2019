# -*- coding: utf-8 -*-

from django.http import JsonResponse

from fyodorpizza.response_codes import BAD_REQUEST, CREATED
from fyodorpizza.usecases.get_menu import GetMenu
from fyodorpizza.usecases.post_order import PostOrder


def get_pizza(request):
    """Receives request and fetches the necessary data."""
    if request.method == 'GET':
        pizza_data = GetMenu()()
        return JsonResponse(pizza_data, safe=False)


def post_order(request):
    """Receives request and saves the necessary data."""
    if request.method == 'POST':
        order_data = request.POST.copy()
        order_data, errors = PostOrder()(order_data)
        if errors:
            return JsonResponse(errors, status=BAD_REQUEST)
        return JsonResponse(order_data, status=CREATED)


def get_statistics(request):
    """Receives request and fetches the necessary data."""
    return JsonResponse({'foo': 'bar'})
