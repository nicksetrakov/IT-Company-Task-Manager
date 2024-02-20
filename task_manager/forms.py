from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.models import Worker, Position, TaskType, Task, Tag


class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class TaskForm(forms.ModelForm):
    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
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
            "tags"
        ]


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select,
        required=False
    )
    field_order = [
        "username",
        "password1",
        "password2",
        "first_name",
        "last_name",
        "position"
    ]

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class WorkerPositionUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select,
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = Worker
        fields = (
            "position",
        )


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password Confirmation'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email'
            })
        }


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Username"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password"}),
    )
