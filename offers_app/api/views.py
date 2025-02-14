from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from offers_app.models import Offer, OfferDetail, Feature
from offers_app.api.serializers import OfferSerializer, OfferDetailSerializer, FeaturesSerializer, OfferCreateUpdateSerializer, GetSingleOfferSerializer, PostSingleOfferSerializer
from offers_app.api.permissions import IsBusinessUser, IsOwnerOrAdmin, IsBusinessOwnerOrReadOnly

from django.db.models import Min, DecimalField
from django.db.models import F

class PageSizePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class offersList(generics.ListCreateAPIView):
    permission_classes = [AllowAny, IsBusinessUser]
    pagination_class = PageSizePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['min_price']

    queryset = Offer.objects.all().order_by('title')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return OfferCreateUpdateSerializer
        return OfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            queryset = queryset.filter(user__user__id=creator_id)

        # queryset = queryset.annotate(min_price=Cast(Min('details__price'), FloatField()))
        queryset = queryset.annotate(min_price=Min('details__price', output_field=DecimalField(max_digits=10, decimal_places=2)))
        queryset = queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days'))
        queryset = queryset.annotate(
            user_first_name=F('user__user__first_name'),
            user_last_name=F('user__user__last_name'),
            user_username=F('user__user__username'),
        )

        delivery_time = self.request.query_params.get("max_delivery_time")
        if delivery_time:
            try:
                delivery_time = int(delivery_time)
            except ValueError:
                delivery_time = None
            if delivery_time is not None:
                queryset = queryset.filter(min_delivery_time__lte=delivery_time)

        return queryset
    
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsBusinessOwnerOrReadOnly]
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer

class DisplayFeatures(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeaturesSerializer

class FeaturesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature
    serializer_class = FeaturesSerializer

class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostSingleOfferSerializer
        return GetSingleOfferSerializer
    
    def post(self, request, *args, **kwargs):
        return Response(
            {"message": "created"}, 
            status=status.HTTP_201_CREATED
        )
        
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()  
        self.check_object_permissions(request, obj)  

        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        old_data = {field: getattr(obj, field) for field in serializer.validated_data}

        serializer.save() 

        updated_data = {
            "id": obj.id,
            "title": obj.title, 
            "details": []
        }

        details_in_request = request.data.get('details', [])

        if not details_in_request:
            return Response(updated_data, status=status.HTTP_200_OK)

        for detail_data in details_in_request:
            detail_id = detail_data.get('id')
            if detail_id:
                try:
                    detail_instance = OfferDetail.objects.get(id=detail_id)
                except OfferDetail.DoesNotExist:
                    continue 

                detail_updated = False
                detail_changes = {}

                for field, value in detail_data.items():
 
                    current_value = getattr(detail_instance, field)
                    if current_value != value:
                        detail_changes[field] = value
                        detail_updated = True
                    else:
                        detail_changes[field] = current_value  

                if detail_updated:
                    detail_changes['id'] = detail_id 
                    updated_data["details"].append(detail_changes)
        
        if not updated_data["details"]:
            return Response(updated_data, status=status.HTTP_200_OK)

        return Response(updated_data, status=status.HTTP_200_OK)