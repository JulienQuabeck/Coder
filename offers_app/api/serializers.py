from offers_app.models import Offer, OfferDetail, Feature, UserProfile
from rest_framework import serializers
from django.db.models import Min

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id']

class OfferDetailSerializer(serializers.ModelSerializer):
    features = serializers.JSONField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

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

class OfferDetailMaximalSerializer(serializers.ModelSerializer):
    features = serializers.JSONField()
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def get_features(self, obj):
        return [feature.name for feature in obj.features.all()]
    
class OfferDetailMaximalWithIdSerializer(serializers.ModelSerializer):
    
    features = serializers.JSONField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def get_features(self, obj):
        return [feature.name for feature in obj.features.all()]

class OfferSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    details = OfferDetailMinimalSerializer(many=True)
    image = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, coerce_to_string=False)
    min_delivery_time = serializers.IntegerField(required=False)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price','min_delivery_time','user_details',
        ]

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
    details = OfferDetailMaximalSerializer(many=True)
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
        validated_data['user'] = self.context['request'].user.userprofile

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features', {})

            offer_detail = OfferDetail.objects.create(
                title=detail_data.get('title'),
                revisions=detail_data.get('revisions'),
                delivery_time_in_days=detail_data.get('delivery_time_in_days'),
                price=detail_data.get('price'),
                offer_type=detail_data.get('offer_type'),
                features=features_data,
            )

            offer.details.add(offer_detail)

        return offer

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model: Feature
        fields = ['name']

class GetSingleOfferSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    details = OfferDetailMaximalWithIdSerializer(many=True)
    image = serializers.FileField(required=False, allow_null=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time',
        ]

    def get_user(self, obj):
        return obj.user.user_id
    
    def get_min_price(self, obj):
        if obj.details.exists():
            min_price = obj.details.aggregate(Min('price'))['price__min']
            return min_price
        return None

    def get_min_delivery_time(self, obj):
        if obj.details.exists():
            min_delivery_time = obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
            return min_delivery_time
        return None 
    
class PostSingleOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailMaximalSerializer(many=True)
    image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
        ]

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        if 'image' in validated_data:
            instance.image = validated_data.get('image', instance.image)
        instance.save()

        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                detail_instance = OfferDetail.objects.get(id=detail_id)
                detail_instance.title = detail_data.get('title', detail_instance.title)
                detail_instance.revisions = detail_data.get('revisions', detail_instance.revisions)
                detail_instance.delivery_time_in_days = detail_data.get(
                    'delivery_time_in_days', detail_instance.delivery_time_in_days
                )
                detail_instance.price = detail_data.get('price', detail_instance.price)
                detail_instance.features = detail_data.get('features', detail_instance.features)
                detail_instance.offer_type = detail_data.get('offer_type', detail_instance.offer_type)
                detail_instance.save()

        return instance
