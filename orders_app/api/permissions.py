from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsRelatedToOrder(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.id == obj.customer_user or 
            request.user == obj.business_user.user
        )
    
class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE' and not (request.user and request.user.is_staff):
            raise PermissionDenied("Only admin users can delete orders.")
        return True