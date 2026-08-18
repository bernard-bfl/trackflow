from rest_framework.permissions import BasePermission

class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.owner == user or user in obj.members.all()


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user