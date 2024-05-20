from django.test import TestCase

from accounts.forms import RegistrationForm, WorkerSearchForm
from accounts.models import Position


class FormsTests(TestCase):
    def test_worker_creation_form_with_first_last_name_is_valid(self) -> None:
        position = Position.objects.create(name="Developer")
        form_data = {
            "email": "test@gmail.com",
            "username": "test_user",
            "password1": "pass123test",
            "password2": "pass123test",
            "first_name": "first",
            "last_name": "last",
            "position": position,
            "agree_terms": True
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_creation_form_with_invalid_data(self) -> None:
        position = Position.objects.create(name="Developer")
        form_data = {
            "username": "test_user",
            "password1": "pass123test",
            "password2": "wrongpassword",
            "first_name": "test",
            "last_name": "test",
            "position": position,
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password2" in form.errors)


class WorkerSearchFormTestCase(TestCase):
    def test_form_worker_valid(self) -> None:
        data = {"username": "test"}
        form = WorkerSearchForm(data=data)
        self.assertTrue(form.is_valid)
