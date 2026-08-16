from rest_framework import permissions


class IsProfile(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем профиля."""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True

        return False


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        return False