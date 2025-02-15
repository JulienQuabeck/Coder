from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_auth_app.models import UserProfile

from offers_app.models import Offer

from additionalfunctions.models import RatingAndReview

from orders_app.models import Orders, OrderDetail
from orders_app.api.serializers import OrderGetSerializer, OrderPostSerializer, OrderCreateUpdateSerializer

from django.http import JsonResponse
from django.db import models
from django.db.models import Avg

class PageSizePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class OrdersList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    #pagination_class = PageSizePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    queryset = Orders.objects.all().order_by('id')

    def get_queryset(self):

        user = self.request.user

        return Orders.objects.filter(
            models.Q(customer_user__user=user) | models.Q(business_user=user.id)
        )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return OrderPostSerializer
        return OrderGetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()

            response_serializer = OrderGetSerializer(order, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SingleOrder(generics.RetrieveUpdateDestroyAPIView):

    queryset = Orders.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def put(self, request, *args, **kwargs):
        return Response({"detail": "PUT method is not allowed. Use PATCH to update the status."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




class OrderInProgressCountList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):

        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            business_user = UserProfile.objects.get(user_id = pk)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count = Orders.objects.filter(business_user = pk, status='in_progress').count()

        return Response({"order_count": order_count}, status=status.HTTP_200_OK)

class CompletedOrderCountList(generics.ListCreateAPIView):

    def get(self, request, pk):
        try:
            business_user = UserProfile.objects.get(user_id = pk)
        except UserProfile.DoesNotExist:
            return Response({"error": "Business user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count = Orders.objects.filter(business_user = pk, status='completed').count()

        return Response({"completed_order_count":order_count}, status=status.HTTP_200_OK)

class BaseInfo(APIView):

    def get(self, request, *args, **kwargs):
        business_user_count = UserProfile.objects.filter(type='business').count()
        offers_count = Offer.objects.all().count()
        review_count = RatingAndReview.objects.all().count()
        average_rating = RatingAndReview.objects.all().aggregate(Avg('rating'))['rating__avg']

        if average_rating is None:
            average_rating = 0
        else:
            average_rating = round(average_rating, 2)

        return Response({'review_count': review_count,'average_rating': average_rating, 'business_profile_count': business_user_count, 'offer_count': offers_count}, status=status.HTTP_200_OK)
        
class CompletedOrdersCounter(APIView):

    def get(self, request):
        completed_order_count = OrderDetail.objects.filter(status='completed').count()
        return JsonResponse({"completed_order_count": completed_order_count}, status=status.HTTP_200_OK)
     