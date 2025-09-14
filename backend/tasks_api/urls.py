from django.urls import path
from tasks_api.lib.api.tasks import TaskListView, TaskSingleView
urlpatterns = [
    path('tasks/', TaskListView.as_view(), name="all-tasks"),  # GET (all), POST
    path('tasks/<int:task_id>', TaskSingleView.as_view(),
         name="single-task"),  # GET (with id), PATCH, DELETE
]
