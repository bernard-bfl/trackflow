from django.db import models
from django.conf import settings

# Create your models here.
class Issue(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'inProgress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'

    class SeverityChoices(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        CRITICAL = 'critical', 'Critical'

    project = models.ForeignKey(
        "projects_app.Project",
        on_delete=models.CASCADE,
        related_name="issues",
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reported_issues",
        null=True,
        blank=True
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=StatusChoices, default=StatusChoices.OPEN,)
    severity = models.CharField(max_length=9, choices=SeverityChoices)
    due_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"
        ordering = ["id"]



class Comment(models.Model):
    issue = models.ForeignKey(
        "issues_app.Issue",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.issue}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]