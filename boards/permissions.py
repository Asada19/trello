from rest_framework import permissions

from boards.models import Member


class IsBoardOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        if Member.objects.filter(user=request.user, board=obj).exists():
            return True
        return False
