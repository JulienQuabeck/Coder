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
        print(f"DEBUG: User = {request.user}, is_staff = {request.user.is_staff}")
        print(f"DEBUG: Request Methode = {request.method}, Objekt User = {obj.user.user}")

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user.is_staff:
                print("DEBUG: Zugriff erlaubt für Admin")
                return True
            
            if isinstance(obj, Offer): 
                is_owner = obj.user.user == request.user
                print(f"DEBUG: Ist Besitzer? {is_owner}")
                return is_owner
            
            print("DEBUG: Zugriff verweigert!")
            return False

        return True



    

class IsBusinessOwnerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.userprofile.type != "business":
            return False

        return obj.user == request.user