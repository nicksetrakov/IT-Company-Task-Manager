from django.test import TestCase

from task_manager.forms import (
    WorkerCreationForm,
    SearchForm,
    WorkerSearchForm,
)
from task_manager.models import Position


class FormsTests(TestCase):
    def test_worker_creation_form_with_first_last_name_is_valid(self):
        position = Position.objects.create(name="Developer")
        form_data = {
            "username": "test_user",
            "password1": "pass123test",
            "password2": "pass123test",
            "first_name": "test",
            "last_name": "test",
            "position": position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_creation_form_with_invalid_data(self):
        position = Position.objects.create(name="Developer")
        form_data = {
            "username": "test_user",
            "password1": "pass123test",
            "password2": "wrongpassword",
            "first_name": "test",
            "last_name": "test",
            "position": position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password2" in form.errors)


class SearchFormTestCase(TestCase):
    def test_form_field_label(self):
        form = SearchForm()
        self.assertEqual(form.fields["name"].max_length, 63)

    def test_form_valid(self):
        data = {"name": "test"}
        form = SearchForm(data=data)
        self.assertTrue(form.is_valid())


class WorkerSearchFormTestCase(TestCase):
    def test_form_worker_valid(self):
        data = {"username": "test"}
        form = WorkerSearchForm(data=data)
        self.assertTrue(form.is_valid)

