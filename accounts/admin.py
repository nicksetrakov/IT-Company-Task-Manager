from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Worker, Position, ActivateToken


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": (
            "first_name", "last_name", "username", "position")}
         ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff", "position"
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(ActivateToken)
class ActivateTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "create_at")
    search_fields = ("user", "token")


admin.site.register(Position)
