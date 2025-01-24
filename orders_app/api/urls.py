from django.urls import path
from orders_app.api.views import OrdersList, SingleOrder


urlpatterns = [
    path('orders/', OrdersList.as_view(), name='orders-list'),
    path('orders/<int:pk>/', SingleOrder.as_view(), name='single-order'),
]