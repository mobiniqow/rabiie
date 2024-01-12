from rest_framework.permissions import BasePermission

from authenticate.models import User


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == User.Role.USER
        except Exception:
            return False


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == User.Role.ADMIN
        except Exception:
            return False


class SuperAdminPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == User.Role.SUPER_ADMIN
        except Exception:
            return False
