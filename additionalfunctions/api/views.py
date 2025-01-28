from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth_app.models import UserProfile

from orders_app.models import Orders

from additionalfunctions.models import RatingAndReview
from additionalfunctions.api.serializers import RatingAndReviewsSerializer

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

class ReviewsView(generics.ListCreateAPIView):
    queryset = RatingAndReview.objects.all()
    serializer_class = RatingAndReviewsSerializer

    def post(self, request, *args, **kwargs):
        serializer = RatingAndReviewsSerializer(data=request.data)
        
        print("Request data:", request.data)
        
        if serializer.is_valid():
            serializer.save()
            print("Serialized data:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer validation failed:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)