from django.urls import path
from additionalfunctions.api.views import OrderInProgressCountList, CompletedOrderCountList, ReviewsView, ReviewSingleView, BaseInfo

urlpatterns = [
   path('order-count/<int:pk>/', OrderInProgressCountList.as_view(), name='order-count'),
   path('completed-order-count/<int:pk>/', CompletedOrderCountList.as_view(), name='completed-order-count'),
   path('reviews/', ReviewsView.as_view(), name='reviews'),
   path('reviews/<int:pk>/', ReviewSingleView.as_view(), name='single-review'),
   path('base-info/', BaseInfo.as_view(), name='base-info'),
]