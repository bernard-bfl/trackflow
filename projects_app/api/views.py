from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from projects_app.models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ProjectWriteSerializer
from .permissions import IsProjectMember, IsProjectOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user
            return Project.objects.filter(
            Q(owner=user) | Q(members=user)
            ).distinct()
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectWriteSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsProjectOwner()]
        return [IsAuthenticated(), IsProjectMember()]

    def create(self, request, *args, **kwargs):
        write_serializer = ProjectWriteSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        project = write_serializer.save(owner=self.request.user)

        read_serializer = ProjectListSerializer(project)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)