from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from offers_app.models import Offer, OfferDetail, Feature
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer, FeaturesSerializer
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

class PageSizePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class offersList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageSizePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['min_price']

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

class FeaturesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature
    serializer_class = FeaturesSerializer