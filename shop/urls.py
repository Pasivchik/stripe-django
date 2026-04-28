from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.get_item, name='get_item'),
    path('buy/<int:id>/', views.get_buy, name='get_buy'),
    path('buy/order/<int:id>/', views.get_order_buy, name='get_order_buy'),
    path('buy/intent/<int:id>/', views.get_payment_intent, name='get_payment_intent'),
]