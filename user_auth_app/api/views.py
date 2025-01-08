from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

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
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

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