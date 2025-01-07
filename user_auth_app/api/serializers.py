from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

        extra_kwargs={
            'password':{
                'write_only': True
            }
        }
    
    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords dont match'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error:':'Email already exists!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        UserProfile.objects.create(user=account, type=self.validated_data['type'])
        return account
    
class UserProfileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='userprofile.type')
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'type']

        