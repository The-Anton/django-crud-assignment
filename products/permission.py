from rest_framework import permissions
from rest_framework import status
from products.utils import MyCustomExcpetion
from django.contrib.auth.mixins import LoginRequiredMixin

UNAUTHENTICATED_MSG = {
    "status": status.HTTP_401_UNAUTHORIZED,
    "message": "No valid authentication credentials were provided!",
}
UNAUTHORIZED_MSG = {
    "status": status.HTTP_403_FORBIDDEN,
    "message": "The endpoint can only be aceesed by staff!",
}
BOX_DELETION_ERROR_MSG = {
    "status": status.HTTP_403_FORBIDDEN,
    "message": "Only the creator of the box can delete it!",
}


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            raise MyCustomExcpetion(
                detail=UNAUTHENTICATED_MSG, status_code=status.HTTP_403_FORBIDDEN
            )


class StaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        else:
            raise MyCustomExcpetion(
                detail=UNAUTHORIZED_MSG, status_code=status.HTTP_403_FORBIDDEN
            )


class PermissionManager(LoginRequiredMixin):
    permission_classes = [
        IsAuthenticated,
    ]
