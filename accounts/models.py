from django.db import models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name="user_accounts",
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_accounts",
        blank=True,
        help_text="Specific permissions for this user.",
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return self.username





class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10)
    profile_image = models.ImageField(
        upload_to='teachers/',
        blank=True,
        null=True
    )
    subjects = models.ManyToManyField(Subject)

    def clean(self):
        if self.subjects.count() > 5:
            raise ValidationError("Max 5 subjects allowed")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"