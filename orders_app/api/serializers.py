from rest_framework import serializers
from orders_app.models import OfferDetail, Orders, OrderDetail
from user_auth_app.models import UserProfile
from rest_framework.response import Response
from rest_framework import status

class OrderGetSerializer(serializers.ModelSerializer):
    customer_user = serializers.IntegerField(source='customer_user.user.id', read_only=True)
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

class OrderPostSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Orders
        fields = ['offer_detail_id']

    def create(self, request, validated_data):
        offer_detail = validated_data.get('offer_detail_id')
        serializer = self.get_serializer(data=request.data)


        if serializer.is_valid():
            order = serializer.save()  # Speichert das Order-Objekt
        
        # Verwende den GET-Serializer für die Rückgabe
            response_serializer = OrderGetSerializer(order, context={'request': request})
        
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     offer = offer_detail.offers.first()
        # except AttributeError:
        #     raise serializers.ValidationError({"offer_id": "No associated Offer found for this OfferDetail."})

        # request_user = self.context['request'].user

        # try:
        #     customer_user_profile = UserProfile.objects.get(user=request_user, type='customer')

        # except UserProfile.DoesNotExist:
        #     raise serializers.ValidationError({"customer_user": "No UserProfile found for the current user."})

        # order = Orders.objects.create(
        #     customer_user=customer_user_profile,
        #     business_user=offer.user.user.id,
        #     offer_detail_id=offer_detail,
        #     status='in_progress',
        # )

        # return order
    
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
            'id', 'customer_user', 'business_user','title','revisions','delivery_time_in_days','price','features',
            'offer_type', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user','title','revisions','delivery_time_in_days','price','features',
            'offer_type', 'created_at', 'updated_at'
        ]

    def get_customer_user(self, obj):

        request_user = self.context.get('request').user

        customer_user_profile = UserProfile.objects.get(user=request_user)

        return customer_user_profile.user_id
    
class OrderInProgressCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id']

class OrderCompletedCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id']
