from django.urls import path
from additionalfunctions.api.views import OrderInProgressCountList, CompletedOrderCountList

urlpatterns = [
   path('order-count/<int:pk>/', OrderInProgressCountList.as_view(), name='order-count'),
   path('completed-order-count/<int:pk>/', CompletedOrderCountList.as_view(), name='completed-order-count'),
   # path('base-info/', BaseInfo.as_view(), name='base-info'),
]