import uuid

from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("created", "создано"),
        ("underway", "в работе"),
        ("completed", "завершено"),
    ]

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID"
    )
    title = models.CharField(
        max_length=100, verbose_name="Название задачи", blank=False, null=False
    )
    description = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Описание задачи"
    )
    status = models.CharField(
        choices=STATUS_CHOICES, default="created", verbose_name="Статус задачи"
    )

    def __str__(self):
        return f"Задача {self.title}. Статус: {self.status}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
