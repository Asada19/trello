from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, obj):
        return obj.owner == request.user

    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated()
