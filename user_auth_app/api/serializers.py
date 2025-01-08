from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
import re

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
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
        errors = {}
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']  
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if pw != repeated_pw:
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append("Passwörter stimmen nicht überein.")
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append("Diese E-Mail-Adresse wird bereits verwendet.")

        if not email:
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append("E-Mail ist erforderlich.")

        if not re.match(email_regex, email):
            if 'email' not in errors:
                errors['email'] = []
            errors['email'].append("Das E-Mail-Format ist ungültig.")

        if User.objects.filter(username=self.validated_data['username']).exists():
            if 'username' not in errors:
                errors['username'] = []
            errors['username'].append("Dieser Benutzername ist bereits vergeben.")

        

        if errors:
            raise serializers.ValidationError(errors)

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

        