from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> Any:
        return reverse("task_manager:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Priority(models.TextChoices):
    URGENT = "urgent", "Urgent"
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


class Task(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.LOW
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    tags = models.ManyToManyField(Tag, related_name="tasks")

    def clean(self) -> None:
        if self.deadline < timezone.now():
            raise ValidationError("The deadline cannot be in the past.")

    def save(
        self, *args, **kwargs
    ) -> None:
        self.full_clean()
        return super().save(
            *args, **kwargs
        )

    def __str__(self) -> str:
        return f"{self.name} {self.deadline} {self.priority}"

    def get_absolute_url(self) -> Any:
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["deadline", "is_completed"]
