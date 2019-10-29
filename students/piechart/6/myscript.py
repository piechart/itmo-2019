from main.models import *

orders = Order.objects.filter(status=OrderType.COOKING)
print(orders)
