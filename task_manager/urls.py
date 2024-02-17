from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
]

app_name = "task_manager"
