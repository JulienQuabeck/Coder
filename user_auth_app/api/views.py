from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserProfileSerializer, FileUploadSerializer, UserDetailSerializer, BusinessUserListSerializer, CustomerUserListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User

from user_auth_app.models import UserProfile, FileUpload

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
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

class RetrievUpdateDestroyDetailUser(generics.RetrieveUpdateDestroyAPIView):
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
        return Response(serializer.data, status=200)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        logged_in_user = request.user.userprofile
        if logged_in_user.type != instance.type:
            return Response(
                {"detail": "Du darfst keine Profile eines anderen Typs ändern oder löschen!"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class ListBusinessUsers(generics.ListCreateAPIView):
    queryset = UserProfile.objects.filter(type="business").distinct()
    serializer_class = BusinessUserListSerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListCustomerUsers(generics.ListCreateAPIView):
    queryset = UserProfile.objects.filter(type="customer").distinct()
    serializer_class = CustomerUserListSerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)