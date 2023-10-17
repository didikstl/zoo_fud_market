from django.urls import path
from apps.order.views import add_to_cart, cart_view

urlpatterns = [
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
]
