from django.urls import path
from .views import IssueViewSet, AssignedToMeView, ReportedByMeView


urlpatterns = [
    path('issues/assigned-to-me/', AssignedToMeView.as_view(), name='issues-assigned-to-me'),
    path('issues/reported-by-me/', ReportedByMeView.as_view(), name='issues-reported-by-me'),
    path('issues/', IssueViewSet.as_view({'post': 'create'}), name='issue-create'),
    path('issues/<int:issueId>/', IssueViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='issue-detail'),
]