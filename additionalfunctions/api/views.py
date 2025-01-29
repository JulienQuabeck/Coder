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

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            business_user_id = self.request.data.get('business_user')
            djangoUser = UserProfile.objects.filter(user_id = business_user_id).first()
            if djangoUser:
                django_user_id = djangoUser.id
                self.request.data['business_user'] = django_user_id
            else:
                print('Keinen Nutzer gefunden')
        elif self.request.method in ['GET']:
            business_user_id = self.request.query_params.get('business_user_id')
            djangoUser = UserProfile.objects.filter(user_id=business_user_id).first()
            if djangoUser:
                self.request.query_params._mutable = True
                self.request.query_params['business_user'] = djangoUser.id
                self.request.query_params._mutable = False
            else:
                print('Keinen Nutzer gefunden')
        return RatingAndReviewsSerializer

        
