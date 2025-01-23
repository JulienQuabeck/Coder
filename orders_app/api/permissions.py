from rest_framework.permissions import BasePermission

class IsRelatedToOrder(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.id == obj.customer_user or 
            request.user == obj.business_user.user
        )