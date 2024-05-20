from django.contrib import admin

from .models import Task, TaskType, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("task_type",)


admin.site.register(TaskType)
admin.site.register(Tag)
