import pytest
from django.core.exceptions import ValidationError

from tasks.models import Task


class TestTaskModel:
    """Тестирование модели Task"""

    def test_task_creation(self, db):
        """Тест создания задачи"""
        task = Task.objects.create(
            title="Новая задача", description="Описание задачи", status="created"
        )

        assert task.uuid is not None
        assert task.title == "Новая задача"
        assert task.status == "created"
        assert Task.objects.count() == 1

    def test_task_default_status(self, db):
        """Тест значения по умолчанию для статуса"""
        task = Task.objects.create(title="Задача без статуса")
        assert task.status == "created"

    def test_task_str_method(self, db):
        """Тест строкового представления"""
        task = Task.objects.create(
            title="Тестовая задача для строкового представления", status="underway"
        )

        assert "Тестовая задача для строкового представления" in str(task)
        assert "Статус: underway" in str(task)

    def test_task_blank_description(self, db):
        """Тест создания задачи без описания"""
        task = Task.objects.create(title="Задача без описания")
        assert task.description is None

    def test_task_invalid_status(self, db):
        """Тест невалидного статуса"""
        task = Task(title="Задача с невалидным статусом")
        task.status = "invalid_status"

        with pytest.raises(ValidationError):
            task.full_clean()

    def test_task_status_choices(self):
        """Тест доступных choices для статуса"""
        status_choices = dict(Task.STATUS_CHOICES)
        assert "created" in status_choices
        assert "underway" in status_choices
        assert "completed" in status_choices
        assert status_choices["completed"] == "завершено"

    def test_task_unique_uuid(self, db):
        """Тест уникальности UUID"""
        task1 = Task.objects.create(title="Задача 1")
        task2 = Task.objects.create(title="Задача 2")

        assert task1.uuid != task2.uuid
