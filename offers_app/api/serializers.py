from offers_app.models import Offer, OfferDetail
from rest_framework import serializers
# from user_auth_app.api.serializers import UserNestedSerializer
from django.contrib.auth.models import User

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = UserNestedSerializer()
    details = OfferDetailSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None