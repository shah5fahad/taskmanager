from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

User = get_user_model()


class TaskAPITestCase(TestCase):
    def setUp(self):
        """Setup test users and client."""
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create(username="user1", email="user1@example.com")
        self.user.set_password("password123")
        self.user.save()

        # Get access token by logging in
        response = self.client.post(
            "/api/login/",
            {"email": "user1@example.com", "password": "password123"},
            format="json",
        )
        self.token = response.data["token"]

        # Set token in headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        # Task API endpoints
        self.create_task_url = "/api/tasks/"
        self.assign_task_url = "/api/tasks/<task_id>/assign/"
        self.get_tasks_url = "/api/users/tasks/"

    def test_create_task(self):
        """Test creating a new task with authentication."""
        data = {
            "name": "Test Task",
            "description": "This is a test task",
            "task_type": "BUG",
            "status": "PENDING",
        }
        response = self.client.post(self.create_task_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_assign_task_to_users(self):
        """Test assigning a task to a user."""
        task = Task.objects.create(
            name="Task 1",
            description="Description 1",
            task_type="FEATURE",
            status="PENDING",
        )

        data = {"email": self.user.email}
        self.assign_task_url = f"/api/tasks/{task.id}/assign/"
        response = self.client.post(self.assign_task_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tasks_for_user(self):
        """Test retrieving all tasks assigned to a user."""
        task = Task.objects.create(
            name="Task 1",
            description="Description 1",
            task_type="PENDING",
            status="IMPROVEMENT",
        )
        task.assigned_users.add(self.user.id)
        self.get_tasks_url = f"/api/users/tasks/?email={self.user.email}"
        response = self.client.get(self.get_tasks_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
