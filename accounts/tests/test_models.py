from django.test import TestCase
from django.urls import reverse

from accounts.models import Position, Worker


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
            reverse("accounts:worker-detail", kwargs={"pk": worker.pk}),
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
