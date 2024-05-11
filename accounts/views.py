from typing import Any

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    HttpResponse
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import (
    WorkerSearchForm,
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    UserLoginForm
)
from accounts.models import Position, Worker
from task_manager.forms import SearchForm


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
    model = Worker
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
    model = Worker

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        context["completed"] = [
            task.name for task in tasks if task.is_completed
        ]
        context["not_completed"] = [
            task.name for task in tasks
            if not task.is_completed
        ]
        return context

    def get_queryset(self) -> Any:
        return (
            super().get_queryset().select_related("position").
            prefetch_related("tasks")
        )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm

    def get_success_url(self) -> Any:
        return reverse_lazy("accounts:worker-detail",
                            kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("accounts:worker-list")


def register(
    request,
) -> HttpResponsePermanentRedirect | HttpResponseRedirect | HttpResponse:
    if request.method == "POST":
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("accounts:login")
        else:
            print("Registration failed!")
    else:
        form = WorkerCreationForm()

    context = {"form": form}
    return render(request, "accounts/sign-up.html", context)


class UserLoginView(LoginView):
    template_name = "accounts/sign-in.html"
    form_class = UserLoginForm


def logout_view(
        request
) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
    logout(request)
    return redirect("accounts:login")
