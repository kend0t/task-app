from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks_api.lib.serializers.tasks_serializer import TaskSerializer
from tasks_api.models import Task
from tasks_api.lib.services.task_services import get_all_tasks, get_task, create_task, update_task, delete_task
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TaskListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all tasks",
        responses={
            200: TaskSerializer(many=True)
        }
    )
    def get(self, request):
        """Endpoint for retrieving all tasks"""
        tasks = get_all_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new task",
        request_body=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: "Invalid or incomplete data"
        }
    )
    def post(self, request):
        """Endpoint for creating a new task"""
        task = create_task(request.data)
        if not task:
            return Response({"message": "Data provided is invalid or incomplete"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskSingleView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve one task by ID",
        manual_parameters=[
            openapi.Parameter(
                "task_id",
                openapi.IN_PATH,
                description="Unique ID of the task to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: TaskSerializer,
            404: "Task not found"
        }

    )
    def get(self, request, task_id):
        """Endpoint for retrieving one task"""
        task = get_task(task_id)
        if not task:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing task by ID",
        manual_parameters=[
            openapi.Parameter(
                "task_id",
                openapi.IN_PATH,
                description="Unique ID of the task to update",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: "Invalid input data",
            404: "Task not found"
        }
    )
    def patch(self, request, task_id):
        """Endpoint for updating an existing task"""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"message": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task = update_task(task_id, request.data)
        if not task:
            return Response({"message": "Data provided is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a task by ID",
        manual_parameters=[
            openapi.Parameter(
                "task_id",
                openapi.IN_PATH,
                description="Unique ID of the task to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            204: "Task successfully deleted",
            400: "Task not found"
        }
    )
    def delete(self, request, task_id):
        """Endpoint for deleting a task"""
        deleted_task = delete_task(task_id)
        if not deleted_task:
            return Response({"message": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Task succesfully deleted"}, status=status.HTTP_204_NO_CONTENT)
