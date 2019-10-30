from django.conf.urls import url
from django.contrib import admin

from main.views import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url('api/pizza', api.get_pizzas),
    url('api/order', api.create_order),
    url('api/statistics/pizza', api.stats),
]
