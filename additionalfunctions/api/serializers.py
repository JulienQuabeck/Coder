from rest_framework import serializers
from orders_app.models import Orders
from additionalfunctions.models import RatingAndReview
from user_auth_app.models import UserProfile
# from models import OrderCount

class UserNestedSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = OrderCount
    #     fields = ['user_id']
    pass

class OrderInProgressCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id']

class OrderCompletedCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id']

class RatingAndReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model= RatingAndReview
        fields = ['business_user','reviewer', 'rating', 'description', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        django_user = UserProfile.objects.filter(id=instance.business_user.id).first()
        if django_user:
            data['business_user'] = django_user.user_id
        return data

    def to_internal_value(self, data):
        business_user_id = data.get('business_user')
        django_user = UserProfile.objects.filter(user_id=business_user_id).first()
        if django_user:
            data['business_user'] = django_user.id
        return super().to_internal_value(data)