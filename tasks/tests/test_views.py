import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db
class TestTaskViews:
    """
    Тесты для API endpoints управления задачами.

    Класс содержит тесты для всех CRUD операций:
    создание, чтение, обновление, удаление и получение списка задач.
    """

    def test_create_task_success(self, api_client, task_data):
        """
        Тест успешного создания задачи через API.

        Проверяет:
        - Корректный HTTP статус 201 Created
        - Сохранение переданных данных в ответе
        - Наличие сгенерированного UUID
        - Фактическое создание записи в базе данных
        """
        url = reverse("tasks:task_create")
        response = api_client.post(url, task_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task_data["title"]
        assert "uuid" in response.data
        assert Task.objects.count() == 1

    def test_create_task_missing_title(self, api_client):
        """
        Тест создания задачи без обязательного поля title.

        Проверяет, что API возвращает ошибку 400 Bad Request
        при попытке создания задачи без названия.
        """
        url = reverse("tasks:task_create")
        data = {"description": "Описание без названия"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_invalid_status(self, api_client):
        """
        Тест создания задачи с недопустимым статусом.

        Проверяет, что API возвращает ошибку 400 Bad Request
        при попытке создания задачи с несуществующим статусом.
        """
        url = reverse("tasks:task_create")
        data = {"title": "Задача", "status": "invalid_status"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_task_success(self, api_client, task_object):
        """
        Тест успешного получения детальной информации о задаче.

        Проверяет:
        - Корректный HTTP статус 200 OK
        - Полноту возвращаемых данных
        - Соответствие данных объекту в базе данных
        """
        url = reverse("tasks:task_detail", kwargs={"pk": task_object.uuid})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Тестовая задача в БД"
        assert response.data["description"] == task_object.description

    def test_retrieve_nonexistent_task(self, api_client, fake_uuid):
        """
        Тест попытки получения несуществующей задачи.

        Проверяет, что API возвращает ошибку 404 Not Found
        при запросе задачи с несуществующим UUID.
        """
        url = reverse("tasks:task_detail", kwargs={"pk": fake_uuid})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_success(self, api_client, task_object):
        """
        Тест успешного обновления задачи.

        Проверяет:
        - Корректный HTTP статус 200 OK
        - Обновление данных в ответе
        - Фактическое изменение данных в базе данных
        - Корректность операции refresh_from_db()
        """
        url = reverse("tasks:task_update", kwargs={"pk": task_object.uuid})

        update_data = {"title": "Новое название", "status": "completed"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Новое название"
        assert response.data["status"] == "completed"

        task_object.refresh_from_db()
        assert task_object.title == "Новое название"

    def test_update_task_invalid_status(self, api_client, task_object):
        """
        Тест попытки обновления с недопустимым статусом.

        Проверяет, что API возвращает ошибку 400 Bad Request
        при попытке обновления задачи с несуществующим статусом.
        """
        url = reverse("tasks:task_update", kwargs={"pk": task_object.uuid})

        update_data = {"title": "Новое название", "status": "invalid_status"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_nonexistent_task(self, api_client, fake_uuid):
        """
        Тест попытки обновления несуществующей задачи.

        Проверяет, что API возвращает ошибку 404 Not Found
        при попытке обновления задачи с несуществующим UUID.
        """
        url = reverse("tasks:task_update", kwargs={"pk": fake_uuid})

        update_data = {"title": "Новое название", "status": "completed"}

        response = api_client.put(url, update_data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task(self, api_client, task_object):
        """
        Тест успешного удаления задачи.

        Проверяет:
        - Корректный HTTP статус 204 No Content
        - Фактическое удаление записи из базы данных
        - Уменьшение счетчика объектов в базе данных
        """
        url = reverse("tasks:task_delete", kwargs={"pk": task_object.uuid})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_delete_nonexistent_task(self, api_client, fake_uuid):
        """
        Тест попытки удаления несуществующей задачи.

        Проверяет, что API возвращает ошибку 404 Not Found
        при попытке удаления задачи с несуществующим UUID.
        """
        url = reverse("tasks:task_delete", kwargs={"pk": fake_uuid})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_task_list_success(self, api_client, multiple_tasks):
        """
        Тест успешного получения списка задач с пагинацией.

        Проверяет:
        - Корректный HTTP статус 200 OK
        - Наличие всех необходимых полей пагинации
        - Корректное количество элементов в results
        - Соответствие общего count количеству созданных задач
        """
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
        """
        Тест получения пустого списка задач.

        Проверяет корректное поведение API при отсутствии задач в базе данных,
        включая нулевые счетчики и отсутствие элементов в results.
        """
        url = reverse("tasks:tasks_list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0
