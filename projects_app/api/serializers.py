from rest_framework import serializers
from auth_app.models import User
from projects_app.models import Project
from auth_app.api.serializers import UserBriefSerializer
from issues_app.api.serializers import IssueBriefSerializer



class ProjectListSerializer(serializers.ModelSerializer):
    ownerId = serializers.IntegerField(source='owner.id')
    memberCount = serializers.SerializerMethodField()
    issueCount = serializers.SerializerMethodField()
    openIssueCount = serializers.SerializerMethodField()
    criticalIssueCount = serializers.SerializerMethodField()

    class Meta:
        model = Project 
        fields = [
            'id',
            'name',
            'memberCount',
            'issueCount',
            'openIssueCount',
            'critcalIssueCount',
            'ownerId',
        ]

    def get_memberCount(self, obj):
        return obj.members.count()

    def get_issueCount(self, obj):
        return obj.issues.count()

    def get_openIssueCount(self, obj):
        return obj.issues.filter(status='open').count()

    def get_criticalIssueCount(self, obj):
        return obj.issues.filter(severity='critical').count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    ownerId = serializers.IntegerField(source='owner.id')
    members = UserBriefSerializer(many=True)
    issues = IssueBriefSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'ownerId', 'members', 'issues']


class ProjectWriteSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Project
        fields = ['name', 'members']