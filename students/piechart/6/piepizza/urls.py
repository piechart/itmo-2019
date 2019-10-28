from django.conf.urls import url
from django.contrib import admin

from main.views import views
from main.views import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', views.cabinet, name="cabinet"),
    url('cabinet', views.cabinet, name="cabinet"),
]
