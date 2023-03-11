from rest_framework.permissions import BasePermission

from user.models import User


class AdministratorPermission(BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.user.is_authenticated
            and request.user.user_type == User.UserType.ADMINISTRATOR
        )
