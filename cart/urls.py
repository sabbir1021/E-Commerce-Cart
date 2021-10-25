from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'cart'

urlpatterns = [

    path('', views.home, name="home"),
    path('s_cart', views.s_cart, name="s_cart"),
   
]