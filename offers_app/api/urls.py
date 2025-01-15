from django.urls import path
from offers_app.api.views import offersList, OfferDetailView


urlpatterns = [
    path('offers/', offersList.as_view(), name='offer-list'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerDetail')
]