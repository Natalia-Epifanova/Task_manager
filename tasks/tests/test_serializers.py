from tasks.serializers import TaskSerializer


class TestTaskSerializer:
    """
    Тесты для сериализатора TaskSerializer.

    Класс содержит тесты для проверки валидации данных,
    преобразования объектов и обработки ошибок в сериализаторе.
    """

    def test_serializer_valid_data(self):
        """
        Тест валидации корректных данных сериализатором.

        Проверяет, что сериализатор принимает и валидирует данные
        с правильными значениями статуса и обязательных полей.
        """
        data = {
            "title": "Сериализованная задача",
            "description": "Описание для сериализации",
            "status": "underway",
        }
        serializer = TaskSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["title"] == data["title"]

    def test_serializer_missing_title(self):
        """
        Тест валидации при отсутствии обязательного поля title.

        Проверяет, что сериализатор корректно определяет отсутствие
        обязательного поля и возвращает соответствующую ошибку.
        """
        data = {"status": "created"}
        serializer = TaskSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_serializer_invalid_status(self):
        """
        Тест валидации недопустимого статуса задачи.

        Проверяет, что сериализатор отклоняет недопустимые значения статуса
        и возвращает понятное сообщение об ошибке.
        """
        data = {"title": "Задача", "status": "invalid_status"}
        serializer = TaskSerializer(data=data)

        assert not serializer.is_valid()
        assert "status" in serializer.errors
        assert 'invalid_status" is not a valid choice.' in str(
            serializer.errors["status"][0]
        )
