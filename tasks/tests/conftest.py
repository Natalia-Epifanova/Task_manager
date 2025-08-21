import pytest
from rest_framework.test import APIClient

from tasks.models import Task


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


@pytest.fixture
def task_data():
    """Данные для создания задачи"""
    return {
        "title": "Тестовая задача",
        "description": "Тестовое описание",
        "status": "created",
    }


@pytest.fixture
def task_object(db):
    """Создание экземпляра задачи в базе данных"""
    return Task.objects.create(
        title="Тестовая задача в БД", description="Описание из БД", status="underway"
    )


@pytest.fixture
def multiple_tasks(db):
    """Создание нескольких задач"""
    tasks = []
    for i in range(3):
        task = Task.objects.create(
            title=f"Задача {i + 1}",
            description=f"Описание {i + 1}",
            status="created" if i % 2 == 0 else "underway",
        )
        tasks.append(task)
    return tasks


@pytest.fixture
def fake_uuid():
    return "12345678-1234-1234-1234-123456789012"
