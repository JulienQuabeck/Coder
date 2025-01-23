from rest_framework import generics
# from additionalfunctions.api.serializers import OrderCountSerializer
# from additionalfunctions.models import Count

class OrderCountList(generics.ListCreateAPIView):
    # queryset = Count.objects.all()
    # serializer_class = OrderCountSerializer
    pass

class CompletedOrderCountList(generics.ListCreateAPIView):
    # queryset = Count.objects.all()
    # serializer_class = OrderCountSerializer
    pass

class BaseInfo(generics.ListCreateAPIView):
    # queryset = Count.objects.all()
    # serializer_class = OrderCountSerializer
    pass


