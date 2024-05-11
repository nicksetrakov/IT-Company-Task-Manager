from django import forms
from django.contrib.auth import get_user_model

from task_manager.models import TaskType, Task, Tag, Priority


class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=Priority.choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "tags",
        ]
