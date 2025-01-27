from rest_framework import serializers
from orders_app.models import Orders
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
