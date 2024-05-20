from django.urls import path

from accounts.views import (
    UserLoginView,
    WorkerRegisterView,
    logout_view,
    PositionListView,
    WorkerListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    WorkerDetailView,
    WorkerPositionUpdateView,
    ActivateAccountView,
    CreateProfileView
)


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", WorkerRegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("", WorkerListView.as_view(), name="worker-list"),
    path(
        "<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "<int:pk>/update/",
        WorkerPositionUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "activate/<str:username>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate"),
    path(
        "create-profile/",
        CreateProfileView.as_view(),
        name="profile-create"
    ),
]

app_name = "accounts"
