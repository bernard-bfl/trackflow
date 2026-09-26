from django.contrib import admin
from .models import Issue, Comment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'project', 'status', 'severity']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'issue', 'author', 'created_at']


