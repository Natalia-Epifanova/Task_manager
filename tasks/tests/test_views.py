import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db
class TestTaskViews:
    """Тестирование API endpoints"""

    def test_create_task_success(self, api_client, task_data):
        """Тест успешного создания задачи"""
        url = reverse("tasks:task_create")
        response = api_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task_data["title"]
        assert "uuid" in response.data
        assert Task.objects.count() == 1

    def test_create_task_missing_title(self, api_client):
        """Тест создания задачи без названия"""
        url = reverse("tasks:task_create")
        data = {"description": "Описание без названия"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_invalid_status(self, api_client):
        """Тест создания задачи с невалидным статусом"""
        url = reverse("tasks:task_create")
        data = {"title": "Задача", "status": "invalid_status"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_task_success(self, api_client, task_object):
        """Тест успешного создания задачи"""
        url = reverse("tasks:task_detail", kwargs={"pk": task_object.uuid})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Тестовая задача в БД"
        assert response.data["description"] == task_object.description

    def test_retrieve_nonexistent_task(self, api_client):
        """Тест получения несуществующей задачи"""
        fake_uuid = "12345678-1234-1234-1234-123456789012"
        url = reverse("tasks:task_detail", kwargs={"pk": fake_uuid})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_success(self, api_client, task_object):
        """Тест обновления задачи"""
        url = reverse("tasks:task_update", kwargs={"pk": task_object.uuid})

        update_data = {"title": "Новое название", "status": "completed"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Новое название"
        assert response.data["status"] == "completed"

        task_object.refresh_from_db()
        assert task_object.title == "Новое название"

    def test_update_task_invalid_status(self, api_client, task_object):
        """Тест обновления задачи"""
        url = reverse("tasks:task_update", kwargs={"pk": task_object.uuid})

        update_data = {"title": "Новое название", "status": "invalid_status"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_nonexistent_task(self, api_client):
        """Тест обновления несуществующей задачи"""
        fake_uuid = "12345678-1234-1234-1234-123456789012"
        url = reverse("tasks:task_update", kwargs={"pk": fake_uuid})

        update_data = {"title": "Новое название", "status": "completed"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task(self, api_client, task_object):
        """Тест удаления задачи"""
        url = reverse("tasks:task_delete", kwargs={"pk": task_object.uuid})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_delete_nonexistent_task(self, api_client):
        """Тест удаления несуществующей задачи"""
        fake_uuid = "12345678-1234-1234-1234-123456789012"
        url = reverse("tasks:task_delete", kwargs={"pk": fake_uuid})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_task_list_success(self, api_client, multiple_tasks):
        """Тест получения списка с задачами"""
        url = reverse("tasks:tasks_list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert len(response.data["results"]) == 3

        assert "count" in response.data
        assert "next" in response.data
        assert "previous" in response.data
        assert "results" in response.data

    def test_get_task_list_empty(self, api_client):
        """Тест получения пустого списка задач"""
        url = reverse("tasks:tasks_list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0
