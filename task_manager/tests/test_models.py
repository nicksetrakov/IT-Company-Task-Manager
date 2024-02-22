from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Worker, Task, TaskType, Position, Tag


class ModelsTests(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEquals(str(position), f"{position.name}")

    def test_create_worker_without_position(self):
        user = Worker.objects.create_user(
            username="test",
            password="passw12345",
            first_name="test",
            last_name="test",
        )
        self.assertIsNotNone(user)

    def test_worker_str(self):
        worker = Worker.objects.create_user(
            username="test",
            password="passw12345",
            first_name="test",
            last_name="test",
        )
        self.assertEquals(
            str(worker),
            f"{worker.username} " f"({worker.first_name} {worker.last_name})",
        )

    def test_worker_get_absolute_url(self):
        worker = Worker.objects.create_user(
            username="test",
            password="passw12345",
            first_name="test",
            last_name="test",
        )
        self.assertEquals(
            worker.get_absolute_url(),
            reverse("task_manager:worker-detail", kwargs={"pk": worker.pk}),
        )

    def test_delete_worker(self):
        worker = Worker.objects.create_user(
            username="test",
            password="passw12345",
            first_name="test",
            last_name="test",
        )
        worker.delete()
        self.assertIsNone(Worker.objects.filter(username="test").first())

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEquals(str(task_type), task_type.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test")
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            priority="High",
            task_type=task_type,
        )
        self.assertEquals(str(task), f"{task.name}"
                                     f" {task.deadline} {task.priority}")

    def test_task_clean_deadline_in_past(self):
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

    def test_tag_str(self):
        tag = Tag.objects.create(name="test")
        self.assertEquals(str(tag), f"{tag.name}")
