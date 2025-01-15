from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from offers_app.models import Offer, OfferDetail, Feature
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer, FeaturesSerializer
from rest_framework import generics



class offersList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

class FeaturesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature
    serializer_class = FeaturesSerializer