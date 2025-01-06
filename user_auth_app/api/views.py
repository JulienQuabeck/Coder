from rest_framework import viewsets
from user_auth_app.models import UserProfile
from .serializers import ProfileSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()  # Alle Profile abrufen
    serializer_class = ProfileSerializer
