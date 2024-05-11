from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        views.PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        views.PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        views.PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("", views.WorkerListView.as_view(), name="worker-list"),
    path(
        "create/",
        views.WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "<int:pk>/update",
        views.WorkerPositionUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "<int:pk>/delete",
        views.WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
]

app_name = "accounts"
