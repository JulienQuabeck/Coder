from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from orders_app.models import Orders
from orders_app.api.serializers import OrderGetSerializer, OrderPostSerializer, OrderCreateUpdateSerializer
from rest_framework.response import Response
from rest_framework import status

class PageSizePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'

class OrdersList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageSizePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    queryset = Orders.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return OrderPostSerializer
        return OrderGetSerializer

class SingleOrder(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Orders.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "PUT method is not allowed. Use PATCH to update the status."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)