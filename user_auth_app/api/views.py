from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserProfileSerializer, FileUploadSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
        else:
            data=serializer.errors

        return Response(data)
    
class GetAllUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class GetDetailUser(generics.RetrieveUpdateDestroyAPIView):
    # queryset = User.objects.all()
    # serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Profil des aktuellen Nutzers abrufen
            user_profile = request.user.userprofile
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"detail": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)

class LoginView(ObtainAuthToken):
    Permission_classes = [AllowAny]

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