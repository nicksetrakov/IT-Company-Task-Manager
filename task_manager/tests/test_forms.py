from django.test import TestCase

from task_manager.forms import SearchForm


class SearchFormTestCase(TestCase):
    def test_form_field_label(self) -> None:
        form = SearchForm()
        self.assertEqual(form.fields["name"].max_length, 63)

    def test_form_valid(self) -> None:
        data = {"name": "test"}
        form = SearchForm(data=data)
        self.assertTrue(form.is_valid())
