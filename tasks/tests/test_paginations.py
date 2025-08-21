import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


@pytest.mark.django_db
class TestTaskPagination:
    """
    Тесты пагинации для списка задач.

    Класс содержит тесты для проверки работы пагинации
    в API endpoints, включая различные сценарии с данными.
    """

    def test_pagination(self, api_client):
        """
        Тест базовой пагинации с данными.

        Проверяет:
        - Корректное разделение данных на страницы
        - Расчет общего количества элементов (count)
        - Наличие ссылки на следующую страницу при необходимости
        - Отсутствие ссылки на предыдущую страницу для первой страницы
        """

        for i in range(7):
            Task.objects.create(
                title=f"Задача {i + 1}",
                description=f"Описание {i + 1}",
                status="created",
            )

        url = reverse("tasks:tasks_list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 7
        assert len(response.data["results"]) == 5
        assert response.data["next"] is not None
        assert response.data["previous"] is None

    def test_pagination_empty_list(self, api_client):
        """
        Тест пагинации пустого списка задач.

        Проверяет корректное поведение пагинации когда в базе данных
        отсутствуют задачи, включая нулевые счетчики и отсутствие навигации.
        """
        url = reverse("tasks:tasks_list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0
        assert response.data["next"] is None
        assert response.data["previous"] is None
