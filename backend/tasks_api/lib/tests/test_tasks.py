import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from tasks_api.models import Task
from rest_framework import status


@pytest.mark.django_db
class TestTaskAPI(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Create Test Case", description="create test case using APITestCase")
        self.task_list_url = reverse("all-tasks")
        self.task_single_url = reverse("single-task", args=[self.task.id])

    # RETRIEVE TASK/S TEST CASES

    def test_get_all_tasks(self):
        """Test case for retrieving all tasks"""

        response = self.client.get(self.task_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_task(self):
        """Test case for retrieving an existing task"""

        response = self.client.get(self.task_single_url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_invalid_task(self):
        """Test case for retrieving an nonexisting task"""

        invalid_url = reverse("single-task", args=[9999999])
        response = self.client.get(invalid_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Task not found"

     # CREATE TASK TEST CASES

    def test_create_task(self):
        """Test case for creating a valid task"""

        data = {"title": "create test case",
                "description": "create test case using APITestCase"}
        response = self.client.post(self.task_list_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_invalid_create_task(self):
        """Test case for creating an invalid task"""

        invalid_data = {"title": "missing description"}
        response = self.client.post(self.task_list_url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Data provided is invalid or incomplete"

    # UPDATE TASK TEST CASES

    def test_update_task(self):
        """ Test case for updating an existing task"""

        data = {"title": "updated title", "is_completed": True}
        response = self.client.patch(self.task_single_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "updated title"

    def test_update_nonexistent_task(self):
        """ Test case for updating a nonexisting task"""

        invalid_url = reverse("single-task", args=[9999999])
        data = {"title": "updated title", "is_completed": True}
        response = self.client.patch(invalid_url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Task not found"

    def test_invalid_update_task(self):
        """Test case for updaating a task with invalid info"""

        invalid_data = {"title": ""}
        response = self.client.patch(
            self.task_single_url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Data provided is invalid"

    # DELETE TASK TEST CASES

    def test_delete_task(self):
        """Test case for deleting an existing task"""

        response = self.client.delete(self.task_single_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "Task succesfully deleted"

    def test_delete_invalid_task(self):
        """Test case for deleting an nonexisting task"""

        invalid_url = reverse("single-task", args=[9999999])
        response = self.client.delete(invalid_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Task not found"
