from django.urls import path
from additionalfunctions.api.views import ReviewsView, ReviewSingleView

urlpatterns = [
   path('reviews/', ReviewsView.as_view(), name='reviews'),
   path('reviews/<int:pk>/', ReviewSingleView.as_view(), name='single-review'),
]