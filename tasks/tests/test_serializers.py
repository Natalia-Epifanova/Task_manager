from tasks.serializers import TaskSerializer


class TestTaskSerializer:
    """Тестирование сериализатора Task"""

    def test_serializer_valid_data(self):
        """Тест валидных данных сериализатора"""
        data = {
            "title": "Сериализованная задача",
            "description": "Описание для сериализации",
            "status": "underway",
        }
        serializer = TaskSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["title"] == data["title"]

    def test_serializer_missing_title(self):
        """Тест отсутствия обязательного поля"""
        data = {"status": "created"}
        serializer = TaskSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_serializer_invalid_status(self):
        """Тест невалидного статуса"""
        data = {"title": "Задача", "status": "invalid_status"}
        serializer = TaskSerializer(data=data)

        assert not serializer.is_valid()
        assert "status" in serializer.errors
        assert 'invalid_status" is not a valid choice.' in str(
            serializer.errors["status"][0]
        )
