from offers_app.models import Offer, OfferDetail, Feature, UserProfile
from rest_framework import serializers
from user_auth_app.api.serializers import UserProfileSerializer
from django.contrib.auth.models import User
from django.db import models

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class OfferDetailSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
    
    def get_features(self, obj):
        return [feature.name for feature in obj.features.all()]
    
    
class OfferDetailMinimalSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerDetail')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    user_details = serializers.SerializerMethodField()
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_delivery_time = serializers.IntegerField(required=False)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]
        read_only_fields = ['min_price', 'min_delivery_time', 'user', 'user_details']

    def get_user_details(self, obj):
        user = obj.user.user 
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
        }
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        user_profile = UserProfile.objects.get(user=user)
        validated_data['user'] = user_profile

        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        detailArray = []
        for detail_data in details_data:
            detail = OfferDetail.objects.create(**detail_data)
            detailArray.add(detail)
        
        offer.min_price = detailArray.aggregate(models.Min('price'))['min_price'] or 0  
        offer.min_delivery_time = detailArray.aggregate(models.Min('delivery_time_in_days'))['min_delivery_time'] or 0 

        offer.save()
        return offer

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model: Feature
        fields = ['id', 'name']