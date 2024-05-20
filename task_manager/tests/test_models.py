from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from task_manager.models import Task, TaskType, Tag, Priority


class ModelsTests(TestCase):

    def test_task_type_str(self) -> None:
        task_type = TaskType.objects.create(name="test")
        self.assertEquals(str(task_type), task_type.name)

    def test_task_str(self) -> None:
        task_type = TaskType.objects.create(name="test")
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            priority=Priority.HIGH,
            task_type=task_type,
        )
        self.assertEquals(str(task), f"{task.name}"
                                     f" {task.deadline} {task.priority}")

    def test_task_clean_deadline_in_past(self) -> None:
        task = Task(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() - timedelta(days=1),
            is_completed=False,
            priority="High",
            task_type=TaskType.objects.create(name="Test Task Type"),
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_tag_str(self) -> None:
        tag = Tag.objects.create(name="test")
        self.assertEquals(str(tag), f"{tag.name}")
