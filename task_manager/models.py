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


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)

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


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    def clean(self) -> None:
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("The deadline cannot be in the past.")

    def save(self,
             force_insert: bool = False,
             force_update: bool = False,
             using: Any | None = None,
             update_fields: Any | None = None) -> None:
        self.full_clean()
        return super(Task, self) \
            .save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f"{self.name} {self.deadline} {self.priority}"

    def get_absolute_url(self) -> Any:
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["deadline", "is_completed"]
