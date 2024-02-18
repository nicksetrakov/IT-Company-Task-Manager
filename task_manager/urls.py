from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("positions/", views.PositionListView.as_view(), name="position-list"),
]

app_name = "task_manager"
