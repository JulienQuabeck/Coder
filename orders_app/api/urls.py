from django.urls import path
from orders_app.api.views import OrdersList, SingleOrder
from orders_app.api.views import OrderInProgressCountList, CompletedOrderCountList, BaseInfo, CompletedOrdersCounter



urlpatterns = [
    path('orders/', OrdersList.as_view(), name='orders-list'),
    path('orders/<int:pk>/', SingleOrder.as_view(), name='single-order'),
    path('order-count/<int:pk>/', OrderInProgressCountList.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountList.as_view(), name='completed-order-count'),
    path('base-info/', BaseInfo.as_view(), name='base-info'),
#     path('completed-order-count/<int:pk>/', CompletedOrdersCounter.as_view(), name='Offer-Complete-Count')
]