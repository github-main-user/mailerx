from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = "USER", "User"
        MANAGER = "MANAGER", "Manager"

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    role = models.CharField(max_length=7, choices=UserRole, default=UserRole.USER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
