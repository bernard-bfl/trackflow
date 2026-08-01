from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['complete_name']

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    complete_name = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        Group,
        related_name='auth_app_users',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='auth_app_users',
        blank=True,
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['complete_name']
