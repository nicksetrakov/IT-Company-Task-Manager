from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Worker, Position

POSITION_URL = reverse("accounts:position-list")
WORKER_URL = reverse("accounts:worker-list")


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
        self.assertTemplateUsed(res, "accounts/position_list.html")


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
        self.assertTemplateUsed(res, "accounts/worker_list.html")
