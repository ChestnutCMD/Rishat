from django.urls import path
from .views import *

urlpatterns = [
    path('buy/<int:id>/', buy_item),
    path('item/<int:id>/', item_detail),
    path('order/<int:id>/', buy_order),
    path('', order_detail),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failed/', payment_failed, name='payment_failed'),
]
