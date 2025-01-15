from offers_app.models import Offer, OfferDetail, Feature
from rest_framework import serializers
from user_auth_app.api.serializers import UserProfileSerializer
from django.contrib.auth.models import User

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class OfferDetailSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def get_price(self, obj):
        return f"{obj.price:.2f}"
    
    def get_features(self, obj):
        return [feature.name for feature in obj.features.all()]

class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerDetail')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = serializers.SerializerMethodField()
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def get_user_details(self, obj):
        user_profile = obj.user_details
        user = user_profile.user

        if user:
            return {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            }
        return {} 

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model: Feature
        fields = ['id', 'name']