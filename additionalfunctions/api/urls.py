from django.urls import path
from additionalfunctions.api.views import OrderInProgressCountList, CompletedOrderCountList, ReviewsView

urlpatterns = [
   path('order-count/<int:pk>/', OrderInProgressCountList.as_view(), name='order-count'),
   path('completed-order-count/<int:pk>/', CompletedOrderCountList.as_view(), name='completed-order-count'),
   path('reviews/', ReviewsView.as_view(), name='reviews'),
   #path('base-info/', BaseInfo.as_view(), name='base-info'),
]