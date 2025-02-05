from user_auth_app.models import UserProfile
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if user_profile and user_profile.type == 'customer':
                return True
            return False
        return True
    
class isOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)
        else:
            print(f"auth. user: {request.user.userprofile.id}")
            print(f"eingeloggter User des Objekts: {request.user.id}")

            try:
                current_user = UserProfile.objects.filter(id = request.user.userprofile.id)
            except UserProfile.DoesNotExist:
                return False
            print(f"current_user: {current_user}")
            print(f"Objekt-reviewer: {obj.reviewer}")
        return bool (request.user and request.user.id == obj.reviewer)