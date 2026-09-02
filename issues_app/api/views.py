from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from issues_app.models import Issue
from .serializers import IssueSerializer, IssueWriteSerializer
from .permissions import IsProjectMemberForIssue, IsReporterOrProjectOwner
from rest_framework import mixins, generics



class IssueViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Issue.objects.all()

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsReporterOrProjectOwner]
        return [IsAuthenticated(), IsProjectMemberForIssue()]
    
    def create(self, request, *args, **kwargs):
        write_serializer = IssueWriteSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        issue = write_serializer.save()

        read_serializer = IssueSerializer(issue)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        write_serializer = IssueWriteSerializer(issue, data=request.data, partial=True)
        write_serializer.is_valid(raise_exception=True)
        issue = write_serializer

        read_serializer = IssueSerializer(issue)
        return Response(read_serializer.data, status=status.HTTP_200_OK)



class AssignedToMeView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(assignee=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReportedByMeView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(reporter=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
