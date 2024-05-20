from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Position, Profile
from task_manager.models import TaskType, Task, Tag, Priority

TASK_URL = reverse("task_manager:task-list")
TAG_URL = reverse("task_manager:tag-list")


class BaseTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            username="test",
            password="passw12345",
            first_name="first",
            last_name="last",
            position=self.position,
        )
        self.user.profile = Profile.objects.create(
            id=1, user=self.user, date_of_birth=date(2020, 1, 1)
        )
        self.client.force_login(self.user)


class PublicTaskTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(BaseTestCase):
    def test_retrieve_task(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            priority=Priority.HIGH,
            task_type=task_type,
        )

        task.assignees.add(self.user)
        task_detail_url = reverse(
            "task_manager:task-detail", kwargs={"pk": task.pk}
        )
        res = self.client.get(task_detail_url)
        self.assertEqual(res.status_code, 200)


class PublicTagTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TAG_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateTagTest(BaseTestCase):
    def test_retrieve_position(self):
        Tag.objects.create(name="test")
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, 200)
        tags = Tag.objects.all()
        self.assertEqual(list(res.context["tag_list"]), list(tags))
        self.assertTemplateUsed(res, "task_manager/tag_list.html")
