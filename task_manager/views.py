from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect, HttpRequest,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import (
    SearchForm,
    TaskForm,
)
from task_manager.models import Task, TaskType, Tag


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_workers = get_user_model().objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> Any:
        queryset = TaskType.objects
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> Any:
        queryset = Task.objects.select_related("task_type")
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self) -> Any:
        return reverse_lazy(
            "task_manager:task-detail",
            kwargs={"pk": self.object.pk}
        )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["assignees"] = self.object.assignees.all()
        return context

    def get_queryset(self) -> Any:
        return (
            super()
            .get_queryset()
            .select_related("task_type")
            .prefetch_related("assignees")
        )


class TaskCompleteView(LoginRequiredMixin, generic.View):
    def post(
        self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        task = Task.objects.get(pk=self.kwargs["pk"])

        task.is_completed = not task.is_completed
        task.save()
        return redirect("task_manager:task-detail", pk=task.pk)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy(Task.get_absolute_url)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> Any:
        queryset = Tag.objects
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task_manager:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task_manager:tag-list")


@login_required
def toggle_assign_to_task(request, pk) -> HttpResponseRedirect:
    worker = get_user_model().objects.get(id=request.user.id)
    if worker.tasks.filter(id=pk):
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(
        reverse_lazy("task_manager:task-detail", args=[pk]))
