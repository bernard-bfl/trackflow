from rest_framework import serializers
from issues_app.models import Issue
from auth_app.api.serializers import UserBriefSerializer

class IssueBriefSerializer(serializers.ModelSerializer):
    assignee = UserBriefSerializer(allow_null=True)
    reporter = UserBriefSerializer(allow_null=True)
    dueDate = serializers.DateField(source='due_date', allow_null=True)
    commentCount = serializers.SerializerMethodField()
    def get_commentCount(self, obj):
        return obj.comments.count()

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'status', 'severity',
            'assignee', 'reporter', 'dueDate', 'commentCount',
        ]