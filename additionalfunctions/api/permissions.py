from rest_framework import permissions
from user_auth_app.models import UserProfile

class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if user_profile and user_profile.type == 'customer':
                return True
            return False
        return True