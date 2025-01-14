from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from offers_app.models import Offer
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer
from rest_framework import generics


class offersList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = 'id'