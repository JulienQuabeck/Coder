from rest_framework import permissions
from user_auth_app.models import UserProfile
from offers_app.models import Offer

class IsBusinessUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if user_profile and user_profile.type == 'business':
                return True
            return False
        return True
    


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ['PUT', 'DELETE']:
            if request.user.is_staff:
                return True
            if isinstance(obj, Offer): 
                return obj.user.user == request.user
            return False
        return True