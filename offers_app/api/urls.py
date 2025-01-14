from django.urls import path
from offers_app.api.views import offersList, OfferDetailView


urlpatterns = [
    path('offers/', offersList.as_view(), name='offer-list'),
    path('offers/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),
]