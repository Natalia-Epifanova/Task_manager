from django.urls import path

from tasks.apps import TasksConfig
from tasks.views import TaskListApiView, TaskRetrieveApiView, TaskCreateApiView, TaskUpdateApiView, TaskDeleteApiView

app_name = TasksConfig.name

urlpatterns = [
    path("", TaskListApiView.as_view(), name="tasks_list"),
    path("<uuid:pk>/", TaskRetrieveApiView.as_view(), name="task_detail"),
    path("create/", TaskCreateApiView.as_view(), name="task_create"),
    path(
        "<uuid:pk>/update/", TaskUpdateApiView.as_view(), name="task_update"
    ),
    path(
        "<uuid:pk>/delete/",
        TaskDeleteApiView.as_view(),
        name="task_delete",
    ),
]