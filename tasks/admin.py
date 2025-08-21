from django.contrib import admin
from django.contrib.admin import ModelAdmin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_filter = ("uuid", "title", "description", "status")
