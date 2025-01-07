from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

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