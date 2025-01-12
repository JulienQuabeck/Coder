from market_app.models import BaseInfo
from rest_framework import serializers
    
class baseInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'businiess_profile_count', 'offer_count']
