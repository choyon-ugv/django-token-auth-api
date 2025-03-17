from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission: 
    - Users can only edit their own profile.
    - Read-only access for others.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user  # Only allow access if the user is the owner
