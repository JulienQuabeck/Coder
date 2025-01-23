from django.urls import path
from orders_app.api.views import OrdersList


urlpatterns = [
    path('orders/', OrdersList.as_view(), name='orders-list'),
]