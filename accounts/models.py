from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from accounts.managers import CustomUserManager
from accounts.utils import create_gravatar_url
from accounts.validators import (
    validate_username,
    validate_name,
    validate_birth_date
)


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    username = models.CharField(
        max_length=30, unique=True, validators=[validate_username]
    )
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, validators=[validate_name])
    last_name = models.CharField(max_length=50, validators=[validate_name])
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="workers",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> Any:
        return reverse("accounts:worker-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)


class Gender(models.TextChoices):
    MALE = "m", "Male"
    FEMALE = "f", "Female"


class Profile(models.Model):
    user = models.OneToOneField(
        Worker, on_delete=models.CASCADE, related_name="profile"
    )
    avatar = models.URLField(max_length=255, blank=True)
    gender = models.CharField(
        max_length=6, choices=Gender.choices, default=Gender.MALE
    )
    date_of_birth = models.DateField(validators=[validate_birth_date])
    info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.avatar:
            self.avatar = create_gravatar_url(self.user.email)
        super().save(*args, **kwargs)


class AbstractToken(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(
        max_length=64, unique=True, default=None, blank=True
    )
    user = models.ForeignKey(Worker, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def verify_token(self, days: int = 1) -> bool:
        validate_exp = timezone.localtime(
            self.create_at
        ) > timezone.now() - timezone.timedelta(days=days)
        return validate_exp

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)
        super().save(*args, **kwargs)


class ActivateToken(AbstractToken):

    class Meta:
        verbose_name_plural = "Activation tokens"

    def __str__(self):
        return f"{self.user}'s token activate: {self.token}"

# It is for future realization
# class PasswordResetToken(AbstractToken):
#     class Meta:
#         verbose_name_plural = "Password reset tokens"
#
#     def __str__(self):
#         return f"{self.user}'s password reset token: {self.token}"
#
#
# class AccessAPIToken(AbstractToken):
#     def __str__(self):
#         return f"{self.user.username}'s API access token"
#
#     class Meta:
#         verbose_name_plural = "API Access Tokens"
