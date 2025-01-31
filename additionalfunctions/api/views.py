from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Avg

from user_auth_app.models import UserProfile

from orders_app.models import Orders

from offers_app.models import Offer

from additionalfunctions.models import RatingAndReview
from additionalfunctions.api.serializers import RatingAndReviewsSerializer
from additionalfunctions.api.permissions import IsCustomerUser

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

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]
 

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            business_user_id = self.request.data.get('business_user')
            djangoUser = UserProfile.objects.filter(user_id=business_user_id).first()

            if djangoUser:
                self.request.data['business_user'] = djangoUser.id
            else:
                print('Keinen Nutzer gefunden')

            if self.request.user.is_authenticated:
                self.request.data['reviewer'] = self.request.user.id
            else:
                print('Benutzer nicht authentifiziert')

        return RatingAndReviewsSerializer

class BaseInfo(APIView):

    def get(self, request, *args, **kwargs):
        business_user_count = UserProfile.objects.filter(type='business').count()
        offers_count = Offer.objects.all().count()
        review_count = RatingAndReview.objects.all().count()
        average_rating = RatingAndReview.objects.all().aggregate(Avg('rating'))['rating__avg']

        if average_rating is None:
            average_rating = 0

        return Response({'review_count': review_count,'average_rating': average_rating, 'business_profile_count': business_user_count, 'offer_count': offers_count})
        
