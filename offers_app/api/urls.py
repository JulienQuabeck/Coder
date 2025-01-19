from django.urls import path
from offers_app.api.views import offersList, OfferDetailView, SingleOfferView


urlpatterns = [
    path('offers/', offersList.as_view(), name='offer-list'),
    path('offers/<int:pk>/', SingleOfferView.as_view(), name='singleOffer'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerDetail')
]