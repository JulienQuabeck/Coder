from rest_framework import serializers
from orders_app.models import Orders

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = [
            'id', 'title',
        ]