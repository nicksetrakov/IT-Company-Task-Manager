from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from task_manager import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("task_manager.urls", namespace="task_manager")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
