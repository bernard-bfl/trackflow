from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from projects_app.models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ProjectWriteSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectWriteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)