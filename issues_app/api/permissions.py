from rest_framework.permissions import BasePermission
from projects_app.models import Project
from issues_app.models import Issue

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



class IsProjectMemberForComment(BasePermission):
    def has_permission(self, request, view):
            issue_id = view.kwargs.get('issueId')
            if not issue_id:
                return True 
            try:
                issue = Issue.objects.get(id=issue_id)
            except Issue.DoesNotExist:
                return True 
            user = request.user 
            return issue.project.owner == user or user in issue.project.members.all()
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.issue.project.owner == user or user in obj.issue.project.members.all()

    


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user