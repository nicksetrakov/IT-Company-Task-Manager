from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from accounts.models import Worker, Position, Profile

POSITION_URL = reverse("accounts:position-list")
WORKER_URL = reverse("accounts:worker-list")


class BaseTestCase(TestCase):
    def setUp(self) -> None:
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


class PublicPositionTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(BaseTestCase):
    def test_retrieve_position(self) -> None:
        Position.objects.create(name="test")
        res = self.client.get(POSITION_URL)
        self.assertEqual(res.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(list(res.context["position_list"]), list(positions))
        self.assertTemplateUsed(res, "accounts/position_list.html")


class PublicWorkerTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(BaseTestCase):
    def test_retrieve_worker(self) -> None:
        res = self.client.get(WORKER_URL)
        self.assertEqual(res.status_code, 200)
        workers = Worker.objects.all()
        self.assertEqual(list(res.context["worker_list"]), list(workers))
        self.assertTemplateUsed(res, "accounts/worker_list.html")
