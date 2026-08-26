from rest_framework import serializers
from issues_app.models import Issue
from projects_app.models import Project
from auth_app.api.serializers import UserBriefSerializer
from auth_app.models import User
class IssueBriefSerializer(serializers.ModelSerializer):
    projectId = serializers.IntegerField(source='project.id')
    assignee = UserBriefSerializer(allow_null=True)
    reporter = UserBriefSerializer(allow_null=True)
    dueDate = serializers.DateField(source='due_date', allow_null=True)
    commentCount = serializers.SerializerMethodField()
    def get_commentCount(self, obj):
        return obj.comments.count()

    class Meta:
        model = Issue
        fields = [
            'id', 'projectId', 'title', 'description', 'status', 'severity',
            'assignee', 'reporter', 'dueDate', 'commentCount',
        ]


class IssueSerializer(serializers.ModelSerializer):
    projectId = serializers.IntegerField(source='project.id')
    assignee = UserBriefSerializer(allow_null=True)
    reporter = UserBriefSerializer(allow_null=True)
    dueDate = serializers.DateField(source='due_date', allow_null=True)
    commentCount = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id', 'projectId', 'title', 'description', 'status', 'severity', 'assignee', 'reporter', 'dueDate', 'commentCount'
        ]

    def get_commentCount(self, obj):
        return obj.comments.count()    


class IssueWriteSerializer(serializers.ModelSerializer):
    projectId = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
    )
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=Issue.StatusChoices.choices)
    severity = serializers.ChoiceField(choices=Issue.SeverityChoices.choices)
    assigneeId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', required=False, allow_null=True)
    reporterId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reporter', required=False)
    dueDate = serializers.DateField(source='date_date', required=False, allow_null=True)

    class Meta:
        model = Issue 
        fields = [
            'id', 'projectId', 'title', 'description', 'status', 'severity', 'assigneeId', 'reporterId', 'dueDate'
        ]