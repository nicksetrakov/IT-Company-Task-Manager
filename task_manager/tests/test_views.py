from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Position
from task_manager.models import TaskType, Task, Tag, Priority

TASK_URL = reverse("task_manager:task-list")
TAG_URL = reverse("task_manager:tag-list")


class PublicTaskTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passw12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_task(self):
        position = Position.objects.create(name="test")
        task_type = TaskType.objects.create(name="Bug")
        worker = get_user_model().objects.create(position=position)
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            priority=Priority.HIGH,
            task_type=task_type,
        )

        task.assignees.add(worker)
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "task_manager/task_list.html")


class PublicTagTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TAG_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateTagTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passw12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_position(self):
        Tag.objects.create(name="test")
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, 200)
        tags = Tag.objects.all()
        self.assertEqual(list(res.context["tag_list"]), list(tags))
        self.assertTemplateUsed(res, "task_manager/tag_list.html")
