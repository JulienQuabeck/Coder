from rest_framework import serializers
from orders_app.models import Orders
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = [
            'id', 'customer_user', 'business_user', 'offer_id', 'status', 'created_at', 'updated_at'
        ]

    def get_offer_id(self, obj):
        pass

class OrderPostSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Orders
        fields = ['offer_detail_id']

    def create(self, validated_data):
        offer_detail_id = validated_data.get('offer_detail_id')

        try:
            # Prüfen, ob das OfferDetail existiert
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError({"offer_detail_id": "OfferDetail with this ID does not exist."})
        
        # Verknüpfte Offer abrufen
        try:
            offer = offer_detail.offers.first()  # Nimm das erste verknüpfte Offer
        except AttributeError:
            raise serializers.ValidationError({"offer_id": "No associated Offer found for this OfferDetail."})

        # Neues Order erstellen
        order = Orders.objects.create(
            customer_user=self.context['request'].user,  # Aktueller Benutzer
            business_user=offer.user,  # Benutzer aus dem Offer
            offer_id=offer_detail.id,
        )

        return order