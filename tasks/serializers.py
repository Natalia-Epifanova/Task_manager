from rest_framework.serializers import ModelSerializer

from tasks.models import Task


class TaskSerializer(ModelSerializer):
    """
    Сериализатор для модели Task.

    Обеспечивает преобразование объектов Task в JSON и обратно.
    Включает валидацию данных и обработку статусов задач.

    Fields:
        Все поля модели Task, поле uuid только для чтения
    """

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("uuid",)
