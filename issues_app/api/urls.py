from django.urls import path
from .views import IssueViewSet, AssignedToMeView, ReportedByMeView, CommentViewSet

urlpatterns = [
    path('issues/assigned-to-me/', AssignedToMeView.as_view(), name='issues-assigned-to-me'),
    path('issues/reported-by-me/', ReportedByMeView.as_view(), name='issues-reported-by-me'),
    path('issues/', IssueViewSet.as_view({'post': 'create'}), name='issue-create'),
    path('issues/<int:issueId>/', IssueViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='issue-detail'),
    path('issues/<int:issueId>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('issues/<int:issueId>/comments/<int:commentId>/', CommentViewSet.as_view({'delete': 'destroy'}), name='comment-detail'),
]