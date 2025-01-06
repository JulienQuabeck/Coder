from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer (serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'type', 'location', 'tel', 'description', 'working_hours', 'file']

