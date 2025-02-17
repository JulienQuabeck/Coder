from user_auth_app.models import UserProfile, FileUpload
from rest_framework import serializers
from django.contrib.auth.models import User
import re
from rest_framework.authentication import TokenAuthentication
from django.conf import settings


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

class FileUploadSerializer(serializers.ModelSerializer):
    # file = serializers.SerializerMethodField()
    
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'location', 'tel', 'description', 'working_hours', 'type', 'created_at', 'file']

    def get_user(self, obj):
        print(obj)
        return {
            "pk": obj.id,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }

class UserDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    file = serializers.SerializerMethodField()
    authentication_classes = [TokenAuthentication] 
    
    class Meta:
        model = UserProfile
        fields = ['user','username','first_name','last_name','file','location', 'tel', 'description', 'working_hours', 'type','email', 'created_at']

    def get_file(self, obj):
        if obj.file:
            return settings.MEDIA_URL + obj.file.name
        return None
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'email' in user_data:
            user.email = user_data['email']
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        
        user.save()

        return super().update(instance, validated_data)

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']

class BusinessUserListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    file = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['id','user', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

    def get_file(self, obj):
        if obj.file:
            return settings.MEDIA_URL + obj.file.name
        return None

class CustomerUserListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    file = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['user', 'file','uploaded_at', 'type']

    def get_file(self, obj):
        if obj.file:
            return settings.MEDIA_URL + obj.file.name
        return None