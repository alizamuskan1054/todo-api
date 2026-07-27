from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Todo


class TodoAPITestCase(APITestCase):
    """
    Har test method 'test_' se start hota hai -> Django/pytest isko
    automatically detect karke run karta hai.
    """

    def setUp(self):
        # Yeh har test se PEHLE chalta hai -> fresh data setup karta hai
        self.todo1 = Todo.objects.create(title="Learn Docker", completed=False)
        self.todo2 = Todo.objects.create(title="Learn CI/CD", completed=True)
        self.list_url = "/api/todos/"

    def test_list_todos(self):
        """GET /api/todos/ -> sare todos wapas aane chahiye"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_todo(self):
        """POST /api/todos/ -> naya todo create ho"""
        payload = {"title": "Learn GitHub Actions", "completed": False}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 3)
        self.assertEqual(response.data["title"], "Learn GitHub Actions")

    def test_create_todo_missing_title_fails(self):
        """Title na ho to validation error aani chahiye (bad input test)"""
        response = self.client.post(self.list_url, {"completed": False})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_single_todo(self):
        """GET /api/todos/{id}/ -> specific todo mile"""
        url = f"{self.list_url}{self.todo1.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Learn Docker")

    def test_update_todo(self):
        """PATCH /api/todos/{id}/ -> completed=True ho jaye"""
        url = f"{self.list_url}{self.todo1.id}/"
        response = self.client.patch(url, {"completed": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)
    def test_create_todo_with_priority(self):
        """Naya field: priority sahi se save honi chahiye"""
        payload = {"title": "Urgent task", "priority": "high"}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["priority"], "high")

    def test_default_priority_is_medium(self):
        """Priority na di jaye to default 'medium' honi chahiye"""
        payload = {"title": "Normal task"}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.data["priority"], "medium")

    def test_delete_todo(self):
        """DELETE /api/todos/{id}/ -> todo remove ho jaye"""
        url = f"{self.list_url}{self.todo2.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 1)

    def test_retrieve_nonexistent_todo_returns_404(self):
        """Galat id -> 404 aana chahiye"""
        response = self.client.get(f"{self.list_url}9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
