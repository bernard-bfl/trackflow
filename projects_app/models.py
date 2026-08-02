from django.db import models
from django.conf import settings

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects",)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="member_projects", blank=True,)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["id"]