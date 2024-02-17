from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from task_manager.models import Worker, Task


def index(request) -> HttpResponse:
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "pages/index.html", context=context)
