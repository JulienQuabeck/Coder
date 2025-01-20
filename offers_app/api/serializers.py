from offers_app.models import Offer, OfferDetail, Feature, UserProfile
from rest_framework import serializers
from user_auth_app.api.serializers import UserProfileSerializer
from django.contrib.auth.models import User
from django.db import models

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id']

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
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'url']
        # fields = ['id', 'url']

class OfferSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    user = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_delivery_time = serializers.IntegerField(required=False)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price','min_delivery_time','user_details',
        ]

    # def get_user(self, obj):
    #     user = obj.user.user
    #     return {
    #         "user": user.pk,
    #     }

    def get_user(self, obj):
        return obj.user.user_id

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

class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
        ]

    def get_user(self, obj):
        return obj.user.user_id

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def create(self, validated_data):
        details_data = validated_data.pop('details', [])

        # Hauptangebot erstellen
        offer = Offer.objects.create(**validated_data)

        # Details hinzufügen
        for detail_data in details_data:
            features_data = detail_data.pop('features', [])  # Erwartet Strings (z. B. ["Logo Design", "Visitenkarte"])

            # Detail mit vollständigen Daten erstellen
            offer_detail = OfferDetail.objects.create(
                title=detail_data.get('title'),
                revisions=detail_data.get('revisions'),
                delivery_time_in_days=detail_data.get('delivery_time_in_days'),
                price=detail_data.get('price'),
                offer_type=detail_data.get('offer_type'),
            )

            # Features hinzufügen, basierend auf den Namen
            feature_objects = Feature.objects.filter(name__in=features_data)
            if len(feature_objects) != len(features_data):  # Validierung der Feature-Namen
                missing_features = set(features_data) - set(feature_objects.values_list('name', flat=True))
                raise serializers.ValidationError(
                    {"features": f"Ungültige Features gefunden: {', '.join(missing_features)}"}
                )

            offer_detail.features.set(feature_objects)
            offer_detail.save()

            # Detail zum Angebot hinzufügen
            offer.details.add(offer_detail)

        return offer

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model: Feature
        fields = ['id', 'name']

class SingleOfferSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def get_user(self, obj):
        return obj.user.user_id