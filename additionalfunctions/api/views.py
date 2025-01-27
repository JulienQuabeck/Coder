from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from user_auth_app.models import UserProfile

from orders_app.models import Orders

from additionalfunctions.models import OrderCount
from additionalfunctions.api.serializers import OrderInProgressCountSerializer

class OrderInProgressCountList(generics.ListCreateAPIView):
    
    def get(self, request, pk):
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

        return Response({"order_count":order_count}, status=status.HTTP_200_OK)

class BaseInfo(generics.ListCreateAPIView):
    pass
    # def get(self, request):
    #     try:
    #         business_user = UserProfile.objects.filter(type='business').count()
    #         return Response({"num:" : business_user}, status=status.HTTP_200_OK)
    #     except UserProfile.DoesNotExist:
    #         return Response({"error": "Business user not found."}, status=status.HTTP_200_OK)



