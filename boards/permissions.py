from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, obj):

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated()
