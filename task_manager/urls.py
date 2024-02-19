from django.urls import path

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path("positions/create/", views.PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", views.PositionDeleteView.as_view(), name="position-delete"),
    path("task-types/", views.TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", views.TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", views.TaskDeleteView.as_view(), name="task-delete"),
    path('tasks/<int:pk>/complete/', views.TaskCompleteView.as_view(), name="task-complete"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete", views.WorkerDeleteView.as_view(), name="worker-delete"),
]

app_name = "task_manager"
