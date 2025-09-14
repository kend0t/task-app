from tasks_api.models import Task
from tasks_api.lib.serializers.tasks_serializer import TaskSerializer


def get_all_tasks():
    """Retrieve all tasks"""
    return Task.objects.all()


def get_task(task_id):
    """Retrieve a single task"""
    return Task.objects.filter(id=task_id).first()


def create_task(task_data):
    """Create a new task"""
    serializer = TaskSerializer(data=task_data)
    if serializer.is_valid():
        return serializer.save()
    return None


def update_task(task_id, task_data):
    """Update the info of an existing task"""
    task = get_task(task_id)
    if not task:
        return None
    serializer = TaskSerializer(task, data=task_data, partial=True)
    if serializer.is_valid():
        return serializer.save()
    return None


def delete_task(task_id):
    """Delete an existing task"""
    task = get_task(task_id)
    if not task:
        return None
    task.delete()
    return True
