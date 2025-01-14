from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserProfileSerializer, FileUploadSerializer, UserDetailSerializer, BusinessUserListSerializer, CustomerUserListSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user_auth_app.models import UserProfile, FileUpload
from rest_framework import serializers


class RegistraionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username':saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            data=serializer.errors

        return Response(data)
    
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post (self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username':user.username,
                'email': user.email,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            error_message = {"detail": ["Falsche Anmeldedaten."]}
            data=serializer.errors

        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)

class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        instance = FileUpload.objects.first()
        serializer = FileUploadSerializer(instance)
        print(f"DEBUG API Response: {serializer.data}")
        return Response(serializer.data)

class GetDetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        user_id = self.kwargs.get('pk')
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            return user_profile
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"detail": "UserProfile not found"})

    def retrieve(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            user = instance.user
            if 'first_name' in request.data:
                user.first_name = request.data['first_name']
            if 'last_name' in request.data:
                user.last_name = request.data['last_name']
            user.save()
            
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class GetAllUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class getBusinessUsers(generics.ListCreateAPIView):
    queryset = UserProfile.objects.filter(type="business").distinct()
    serializer_class = BusinessUserListSerializer

class getCustomerUsers(generics.ListCreateAPIView):
    queryset = UserProfile.objects.filter(type="customer").distinct()
    serializer_class = CustomerUserListSerializer