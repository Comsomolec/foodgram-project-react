from rest_framework import permissions


class Author(permissions.BasePermission):
    """Вносить изменения может только автор"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CurrentUser(permissions.BasePermission):
    """Вносить изменения может только текущий пользователь"""
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
