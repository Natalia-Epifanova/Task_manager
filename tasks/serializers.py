from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tasks.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ('uuid',)

    @staticmethod
    def validate_status(value):
        if value not in dict(Task.STATUS_CHOICES):
            raise serializers.ValidationError("Неверный статус задачи")
        return value