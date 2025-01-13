from user_auth_app.models import UserProfile, FileUpload
from rest_framework import serializers
from django.contrib.auth.models import User
import re
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):#benötigt
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

class FileUploadSerializer(serializers.ModelSerializer):#benötigt
    # file = serializers.SerializerMethodField()

    # class Meta:
    #     model = FileUpload
    #     fields = ['file', 'uploaded_at']

    file = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']

    def get_file(self, obj):
        if obj.file:
            return settings.MEDIA_URL + obj.file.name
        return None

class UserProfileSerializer(serializers.ModelSerializer):#benötigt
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'location', 'tel', 'description', 'working_hours', 'type', 'created_at', 'file']

    def get_user(self, obj):
        return {
            "pk": obj.id,
            "username": obj.username,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
        }

class UserDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    file = serializers.SerializerMethodField()
    authentication_classes = [TokenAuthentication] 
    
    class Meta:
        model = UserProfile
        fields = ['user','username','first_name','last_name','file','location', 'tel', 'description', 'working_hours', 'type','email', 'created_at']

    def get_file(self, obj):
        # Zugriff auf das file-Feld des UserProfile-Objekts
        if obj.file:  # Überprüfen, ob das file-Feld existiert
            return settings.MEDIA_URL + obj.file.name  # Relativer Pfad der Datei
        return None









class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']

# class UserDetailSerializer(serializers.ModelSerializer):
#     user = serializers.IntegerField(source='user.id', read_only=True)
#     email = serializers.CharField(source='user.email', read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
#     first_name = serializers.CharField(source='user.first_name', read_only=True)
#     last_name = serializers.CharField(source='user.last_name', read_only=True)
#     authentication_classes = [TokenAuthentication] 
    
#     class Meta:
#         model = UserProfile
#         fields = ['user','username','first_name','last_name', 'email', 'location', 'tel', 'description', 'working_hours', 'type', 'created_at', 'file']

class BusinessUserListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'file', 'location', 'tel', 'description', 'working_hours', 'type']
    
class CustomerUserListSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'file','uploaded_at', 'type']

    def get_user(self, obj):
        return obj
    
class BusinessUserDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    authentication_classes = [TokenAuthentication] 
    
    class Meta:
        model = UserProfile
        fields = ['user_id','username','first_name','last_name', 'email', 'location', 'tel', 'description', 'working_hours', 'type', 'created_at', 'file']     