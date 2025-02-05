from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from orders_app.models import Orders
from orders_app.api.serializers import OrderGetSerializer, OrderPostSerializer, OrderCreateUpdateSerializer

from django.db import models

class PageSizePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class OrdersList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageSizePagination
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
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