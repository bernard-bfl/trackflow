from rest_framework.permissions import BasePermission
from projects_app.models import Project

class IsProjectMemberForIssue(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        project_id = request.data.get('projectId')
        if not project_id:
            return True
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return True
        return project.owner == request.user or request.user in project.members.all()

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.project.owner == user or user in obj.project.members.all()


class IsReporterOrProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.reporter == user or obj.project.owner == user