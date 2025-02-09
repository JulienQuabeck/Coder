from rest_framework import generics, permissions

from user_auth_app.models import UserProfile

from additionalfunctions.models import RatingAndReview
from additionalfunctions.api.serializers import RatingAndReviewsSerializer, RatingAndReviewsSingleSerializer
from additionalfunctions.api.permissions import IsCustomerUser, isOwnerOrAdmin
 
class ReviewsView(generics.ListCreateAPIView):
    queryset = RatingAndReview.objects.all()
    serializer_class = RatingAndReviewsSerializer  

    def get_queryset(self):
        queryset = super().get_queryset()

        business_user_id = self.request.query_params.get("business_user_id")
        reviewer_id = self.request.query_params.get("reviewer_id")

        if business_user_id:
            queryset = queryset.filter(business_user__user__id=business_user_id)

        if reviewer_id:
            queryset = queryset.filter(reviewer=reviewer_id) 

        ordering = self.request.query_params.get('ordering', None)
        if ordering in ['rating', '-rating', 'updated_at', '-updated_at']:
            queryset = queryset.order_by(ordering) 

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        if self.request.method == ['PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
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

class ReviewSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RatingAndReview.objects.all()
    serializer_class = RatingAndReviewsSingleSerializer  

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [isOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.request.method in ['PATCH']:
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
    