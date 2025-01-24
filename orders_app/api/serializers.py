from rest_framework import serializers
from orders_app.models import OfferDetail, Orders, OrderDetail
from user_auth_app.models import UserProfile

class OrderGetSerializer(serializers.ModelSerializer):
    customer_user = serializers.SerializerMethodField()
    title = serializers.CharField(source='offer_detail_id.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail_id.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail_id.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail_id.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(source='offer_detail_id.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail_id.offer_type', read_only=True)

    class Meta:
        model = Orders
        fields = [
            'id', 'customer_user', 'business_user','title','revisions','delivery_time_in_days','price','features','offer_type', 'status', 'created_at', 'updated_at'
        ]

    def get_customer_user(self, obj):

        request_user = self.context.get('request').user

        customer_user_profile = UserProfile.objects.get(user=request_user)

        return customer_user_profile.user_id

class OrderPostSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)  # Ich verwende PrimaryKeyRelatedField

    class Meta:
        model = Orders
        fields = ['offer_detail_id']

    def create(self, validated_data):
        offer_detail = validated_data.get('offer_detail_id')  # Das OfferDetail-Objekt wird direkt zugewiesen

        # Hole das zugehörige Angebot für das OfferDetail
        try:
            offer = offer_detail.offers.first()  # Hier wird das zugehörige Angebot gefunden
        except AttributeError:
            raise serializers.ValidationError({"offer_id": "No associated Offer found for this OfferDetail."})

        request_user = self.context['request'].user

        try:
            customer_user_profile = UserProfile.objects.get(user=request_user)

        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"customer_user": "No UserProfile found for the current user."})

        # Erstelle die Bestellung
        order = Orders.objects.create(
            customer_user=customer_user_profile,
            business_user=offer.user.user.id,  # Geschäftskonto-ID
            offer_detail_id=offer_detail,  # Hier übergebe ich das vollständige OfferDetail-Objekt
            status='in_progress',  # Status setzen
        )

        return order
    
class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    
    customer_user = serializers.SerializerMethodField()
    title = serializers.CharField(source='offer_detail_id.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail_id.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail_id.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail_id.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(source='offer_detail_id.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail_id.offer_type', read_only=True)

    class Meta:
        model = OrderDetail
        fields = [
            'id', 'customer_user', 'business_user','title','revisions','delivery_time_in_days','price','features','offer_type', 'status', 'created_at', 'updated_at'
        ]

    def get_customer_user(self, obj):

        request_user = self.context.get('request').user

        customer_user_profile = UserProfile.objects.get(user=request_user)

        return customer_user_profile.user_id