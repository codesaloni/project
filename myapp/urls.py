from django.urls import path
from .views import *


urlpatterns = [
    path('index/',register,name="register"),
    path('login/', login, name='login'),
    path('home/',home,name="home"),
    path('product/',product,name="product"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/',view_cart, name='view_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
 
    
]