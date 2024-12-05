"""
Database models.
"""
from enum import Enum
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class RoleKey(Enum):
    STAFF = 'STAFF'  # Staff
    SUPERVISOR = 'SUPERVISOR'  # Supervisor
    ADMIN = 'ADMIN'  # Admin


class RoleName(Enum):
    STAFF = 'STAFF'
    SUPERVISOR = 'SUPERVISOR'
    ADMIN = 'ADMIN'


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Unique phone number
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)  # Registered status (default: False)
    image_uploaded = models.BooleanField(default=False)  # Image uploaded status (default: False)
    experience = models.FloatField(default=0.0)  # Experience in years, default is 0.0
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')  # Foreign key to Role

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Role(models.Model):
    """Role for each user."""
    role_name = models.CharField(
        max_length=255,
        choices=[(tag.name, tag.value) for tag in RoleName],  # Choices for role_name
        default=RoleName.STAFF.value  # Default role_name as "STAFF"
    )

    # Many-to-many relationship with Permission
    permissions = models.ManyToManyField('Permission', related_name='roles')

    def __str__(self):
        return self.role_name


class Permission(models.Model):
    """Permission for roles."""
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]

    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default='GET'
    )  # HTTP method associated with the permission
    name = models.CharField(max_length=255, unique=True)  # Permission name
    url = models.CharField(max_length=500)  # URL associated with the permission
    description = models.TextField(null=True, blank=True)  # Optional description for the permission

    def __str__(self):
        return f'{self.name} ({self.method}) - {self.url}'

class Book(models.Model):
    """Basic book model."""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)  # ISBN number
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title} by {self.author}'