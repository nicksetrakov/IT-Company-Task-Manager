from django.test import TestCase
from django.urls import reverse

from accounts.models import Position, Worker


class ModelsTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "password123!M",
        }

    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEquals(str(position), f"{position.name}")

    def test_create_worker_without_position(self):
        worker = Worker.objects.create_user(**self.user_data)
        self.assertIsNotNone(worker)

    def test_worker_str(self):
        worker = Worker.objects.create_user(**self.user_data)
        self.assertEquals(
            str(worker),
            f"{worker.username} " f"({worker.first_name} {worker.last_name})",
        )

    def test_worker_get_absolute_url(self):
        worker = Worker.objects.create_user(**self.user_data)
        self.assertEquals(
            worker.get_absolute_url(),
            reverse("accounts:worker-detail", kwargs={"pk": worker.pk}),
        )

    def test_delete_worker(self):
        worker = Worker.objects.create_user(**self.user_data)
        worker.delete()
        self.assertIsNone(Worker.objects.filter(username="test").first())
