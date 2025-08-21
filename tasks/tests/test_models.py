import pytest
from django.core.exceptions import ValidationError

from tasks.models import Task


class TestTaskModel:
    """
    Тесты для модели Task.

    Класс содержит тесты для проверки функциональности модели задач,
    включая создание, валидацию, значения по умолчанию и строковое представление.
    """

    def test_task_creation(self, db):
        """
        Тест успешного создания задачи в базе данных.

        Проверяет:
        - Создание задачи с всеми обязательными полями
        - Автогенерацию UUID
        - Корректное сохранение атрибутов
        - Увеличение счетчика объектов в базе данных
        """
        task = Task.objects.create(
            title="Новая задача", description="Описание задачи", status="created"
        )

        assert task.uuid is not None
        assert task.title == "Новая задача"
        assert task.status == "created"
        assert Task.objects.count() == 1

    def test_task_default_status(self, db):
        """
        Тест значения статуса по умолчанию.

        Проверяет, что при создании задачи без указания статуса
        автоматически устанавливается статус 'created'.
        """
        task = Task.objects.create(title="Задача без статуса")
        assert task.status == "created"

    def test_task_str_method(self, db):
        """
        Тест строкового представления объекта задачи.

        Проверяет, что метод __str__ возвращает корректную строку,
        содержащую название задачи и ее статус.
        """
        task = Task.objects.create(
            title="Тестовая задача для строкового представления", status="underway"
        )

        assert "Тестовая задача для строкового представления" in str(task)
        assert "Статус: underway" in str(task)

    def test_task_blank_description(self, db):
        """
        Тест создания задачи без описания.

        Проверяет, что поле description может быть пустым (null=True, blank=True)
        и по умолчанию устанавливается в None.
        """
        task = Task.objects.create(title="Задача без описания")
        assert task.description is None

    def test_task_invalid_status(self, db):
        """
        Тест валидации недопустимого статуса задачи.

        Проверяет, что попытка установить недопустимый статус
        вызывает исключение ValidationError при вызове full_clean().
        """
        task = Task(title="Задача с невалидным статусом")
        task.status = "invalid_status"

        with pytest.raises(ValidationError):
            task.full_clean()

    def test_task_status_choices(self):
        """
        Тест доступных вариантов выбора для статуса задачи.

        Проверяет, что все ожидаемые статусы присутствуют в STATUS_CHOICES
        и имеют корректные русскоязычные описания.
        """
        status_choices = dict(Task.STATUS_CHOICES)
        assert "created" in status_choices
        assert "underway" in status_choices
        assert "completed" in status_choices
        assert status_choices["completed"] == "завершено"

    def test_task_unique_uuid(self, db):
        """
        Тест уникальности UUID для каждой задачи.

        Проверяет, что каждая создаваемая задача получает уникальный UUID,
        гарантируя отсутствие коллизий идентификаторов.
        """
        task1 = Task.objects.create(title="Задача 1")
        task2 = Task.objects.create(title="Задача 2")

        assert task1.uuid != task2.uuid
