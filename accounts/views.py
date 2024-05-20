from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import RedirectURLMixin
from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    HttpRequest,
)
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic
from django.views.generic import View, FormView

from accounts.forms import (
    WorkerSearchForm,
    RegistrationForm,
    WorkerPositionUpdateForm,
    UserLoginForm,
    ProfileForm,
)
from accounts.models import Position, Worker, ActivateToken, Profile
from accounts.services import AccountsEmailNotification
from task_manager.forms import SearchForm


User = get_user_model()


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> Any:
        queryset = Position.objects
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("accounts:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("accounts:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("accounts:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> Any:
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "accounts/worker_detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tasks = self.object.user.tasks.all()
        context["completed"] = [
            task.name for task in tasks if task.is_completed
        ]
        context["not_completed"] = [
            task.name for task in tasks if not task.is_completed
        ]
        return context

    def get_queryset(self) -> Any:
        return (
            super()
            .get_queryset()
            .select_related("user__position")
            .prefetch_related("user__tasks")
        )


class WorkerRegisterView(generic.CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect("task_manager:index")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        user_token = ActivateToken.objects.create(user=user)

        activate_url = (
            f"{self.request.scheme}://{self.request.get_host()}"
            f"""{reverse(
                'accounts:activate',
                args=[user.username, user_token.token]
            )}"""
        )

        email_service = AccountsEmailNotification()
        email_service.send_activation_email(
            user.email, user.get_full_name(), activate_url
        )

        messages.info(
            self.request,
            "Registration completed. "
            "Please check your email to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm

    def get_success_url(self) -> Any:
        return reverse_lazy(
            "accounts:worker-detail", kwargs={"pk": self.object.pk}
        )


class UserLoginView(RedirectURLMixin, FormView):
    template_name = "accounts/sign-in.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data.get("remember_me")
        user = authenticate(self.request, email=email, password=password)
        if not user:
            messages.error(self.request, "Invalid login or password")
            return redirect("accounts:login")

        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            self.request.session.set_expiry(0)

        login(self.request, user)
        messages.success(self.request, "You have successfully logged in")

        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url, settings.ALLOWED_HOSTS
        ):
            return redirect(iri_to_uri(next_url))

        return redirect("task_manager:index")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid login or password")
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(
        request
) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
    logout(request)
    return redirect("accounts:login")


class ActivateAccountView(View):
    def get(self, request: HttpRequest, username: str, token: str):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(ActivateToken, token=token, user=user)

        if user.is_active:
            messages.error(request, "User is already activated")
            return redirect("task_manager:index")

        if token.verify_token():
            user.is_active = True
            token.delete()
            user.save()

            messages.success(request, "Activation complete")
            return redirect("task_manager:index")

        messages.error(request, "Token expired")
        return redirect("task_manager:index")


class CreateProfileView(LoginRequiredMixin, FormView):
    template_name = "accounts/create_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("task_manager:index")

    def get_initial(self):
        initial = super().get_initial()

        profile_picture = self.request.session.get("profile_picture")
        if profile_picture:
            initial["avatar"] = profile_picture

        return initial

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.id = self.request.user.id
        profile.user = self.request.user
        profile.save()

        self.request.session.pop("profile_picture", None)
        return super().form_valid(form)
