import json

from django.http import JsonResponse
from main.models import *
from datetime import strptime

def get_pizzas(request):
    response = {
        "pizzas": [pizza.as_dict() for pizza in Pizza.objects.all()]
    }
    return JsonResponse(response)
    
def create_order(request):
    def resolve_pizza(pizza_title):
        pizza = Pizza.objects.get(title=pizza_title)
        if pizza is not None:
            return pizza
        return None
        
    date = request.POST.get('date')
    address = request.POST.get('address')
    email = request.POST.get('email')
    
    pizza_titles = request.POST.get('pizzas').split(',')
    pizza_items = map(lambda title: resolve_pizza(title), pizza_titles)
    pizzas = [pizza for pizza in pizza_items if pizza is not None]
    if not pizzas:
        return JsonResponse({
            "result": "error",
            "error": "no valid pizzas provided"
        })
    
    order = Order(
        "place_date": strptime(date, '%y-%m-%d'),
        "pizzas": pizzas,
        "delivery_address": address,
        "customer_email": email,
        "status": "ACCEPTED"
    )
    order.save()
    return JsonResponse({
        "result": "success",
        "order_id": order.pk
    })

def stats(request):
    TODO