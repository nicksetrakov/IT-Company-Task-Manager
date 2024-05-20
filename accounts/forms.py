from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _

from accounts.models import Position, Profile

User = get_user_model()


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class RegistrationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects, widget=forms.Select, required=False
    )
    agree_terms = forms.BooleanField(
        required=True,
        label="I agree all statements in Terms of service",
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "position"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control form-control-lg"}
            )
            if field_name == "agree_terms":
                field.widget.attrs.update({"class": "form-check-input me-2"})
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"


class WorkerPositionUpdateForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects, widget=forms.Select, required=False
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("position",)


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter a valid email address",
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password"
            }
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "rememberMe"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing_classes = field.widget.attrs.get("class", "")
                if "is-invalid" not in existing_classes:
                    field.widget.attrs["class"] = (
                        f"{existing_classes} is-invalid"
                    )


class DateInputCustom(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {}
        if options is None:
            options = {}
        attrs.update(
            {"class": "form-control mb-3", "data-date-format": "yyyy-mm-dd"}
        )
        attrs.update(options)
        super().__init__(attrs=attrs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("gender", "date_of_birth", "avatar", "info")

        labels = {
            "date_of_birth": "Date of your Birth",
            "avatar": "Avatar URL"
        }

        placeholders = {
            "avatar": "Left empty to use gravatar",
            "info": "Enter some additional information",
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control form-control-lg",
                    "placeholder": self.Meta.placeholders.get(field_name),
                }
            )
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        self.fields["date_of_birth"].widget = DateInputCustom()
        if self.errors.get("date_of_birth"):
            self.fields["date_of_birth"].widget.attrs["class"] += " is-invalid"
