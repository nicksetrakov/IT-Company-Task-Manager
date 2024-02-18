from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path("positions/create", views.PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete", views.PositionDeleteView.as_view(), name="position-delete"),
]

app_name = "task_manager"
