from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)





class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['complete_name']

    objects = CustomUserManager()

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
