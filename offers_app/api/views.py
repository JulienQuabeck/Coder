from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from offers_app.models import Offer, OfferDetail, Feature
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer, FeaturesSerializer, OfferCreateUpdateSerializer
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min
from django.db.models import F

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
    #serializer_class = OfferSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return OfferCreateUpdateSerializer
        return OfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(min_price=Min('details__price'))
        queryset = queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days'))
        queryset = queryset.annotate(
            user_first_name=F('user__user__first_name'),
            user_last_name=F('user__user__last_name'),
            user_username=F('user__user__username')
        )
        return queryset

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

class FeaturesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature
    serializer_class = FeaturesSerializer