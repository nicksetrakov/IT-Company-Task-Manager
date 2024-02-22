from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Worker, Position, TaskType, Task, Tag

POSITION_URL = reverse("task_manager:position-list")
TASK_URL = reverse("task_manager:task-list")
WORKER_URL = reverse("task_manager:worker-list")
TAG_URL = reverse("task_manager:tag-list")


class PublicPositionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passw12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_position(self):
        Position.objects.create(name="test")
        res = self.client.get(POSITION_URL)
        self.assertEqual(res.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(list(res.context["position_list"]), list(positions))
        self.assertTemplateUsed(res, "task_manager/position_list.html")


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
        worker = Worker.objects.create(position=position)
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline=timezone.now() + timedelta(days=1),
            is_completed=False,
            priority="High",
            task_type=task_type,
        )

        task.assignees.add(worker)
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "task_manager/task_list.html")


class PublicWorkerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passw12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_worker(self):
        res = self.client.get(WORKER_URL)
        self.assertEqual(res.status_code, 200)
        worker = Worker.objects.all()
        self.assertEqual(list(res.context["worker_list"]), list(worker))
        self.assertTemplateUsed(res, "task_manager/worker_list.html")


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
