from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse,
    HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from googleapiclient.errors import HttpError

from task_manager.forms import (
    SearchForm,
    TaskForm,
)
from task_manager.models import Task, TaskType, Tag
from task_manager.utils import (
    get_credentials,
    create_google_task,
    update_google_task,
    delete_google_task,
)


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:task-list")

    def form_valid(self, form) -> HttpResponseRedirect:
        response = super().form_valid(form)
        task = self.object

        creds = get_credentials()

        try:
            google_task = create_google_task(task, creds)
            task.google_task_id = google_task["id"]
            task.save()
        except HttpError as error:
            print(f"An error occurred: {error}")

        return response


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"

    def get_success_url(self) -> Any:
        return reverse_lazy(
            "task_manager:task-detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form: TaskForm) -> HttpResponse:
        response = super().form_valid(form)
        task = self.object

        creds = get_credentials()

        try:
            updated_task_body = {
                "id": task.google_task_id,
                "title": task.name,
                "notes": task.description,
                "due": task.deadline.isoformat(),
            }
            updated_task = update_google_task(
                task.google_task_id, updated_task_body, creds
            )
            task.google_task_id = updated_task["id"]
            task.save()
        except HttpError as error:
            print(f"An error occurred: {error}")

        return response


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


class TaskCompleteView(LoginRequiredMixin, View):
    def post(
            self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        task = get_object_or_404(Task, pk=self.kwargs["pk"])

        creds = get_credentials()
        task.is_completed = not task.is_completed

        try:
            if task.is_completed:
                if task.google_task_id:
                    update_google_task(
                        task.google_task_id,
                        {"id": task.google_task_id, "status": "completed"},
                        creds,
                    )
            else:
                if task.google_task_id:
                    update_google_task(
                        task.google_task_id,
                        {"id": task.google_task_id, "status": "needsAction"},
                        creds,
                    )
        except HttpError as error:
            print(f"An error occurred: {error}")

        task.save()
        return redirect("task_manager:task-detail", pk=task.pk)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")

    def delete(self, request, *args, **kwargs) -> HttpResponseRedirect:
        task = self.get_object()
        creds = get_credentials()

        try:
            delete_google_task(task.google_task_id, creds)
        except HttpError as error:
            print(f"An error occurred: {error}")

        return super().delete(request, *args, **kwargs)


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


class ToggleAssignToTaskView(LoginRequiredMixin, View):
    def get(
            self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        worker = request.user
        task = get_object_or_404(Task, pk=self.kwargs["pk"])

        creds = get_credentials()

        if worker.tasks.filter(id=self.kwargs["pk"]).exists():
            worker.tasks.remove(task)
            if task.google_task_id:
                try:
                    delete_google_task(task.google_task_id, creds)
                    task.google_task_id = None
                    task.save()
                except HttpError as error:
                    print(f"An error occurred: {error}")
        else:
            worker.tasks.add(task)
            if task.google_task_id:
                try:
                    delete_google_task(task.google_task_id, creds)
                except HttpError as error:
                    print(f"An error occurred: {error}")
            try:
                google_task = create_google_task(task, creds)
                task.google_task_id = google_task["id"]
                task.save()
            except HttpError as error:
                print(f"An error occurred: {error}")

        return redirect("task_manager:task-detail", pk=self.kwargs["pk"])
