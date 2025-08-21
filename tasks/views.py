from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from tasks.models import Task
from tasks.paginations import CustomPagination
from tasks.serializers import TaskSerializer


class TaskCreateApiView(CreateAPIView):
    """
    API endpoint для создания новой задачи.

    Methods:
        POST: Создание новой задачи

    Request Body:
        - title (str): Название задачи (обязательное)
        - description (str): Описание задачи (опциональное)
        - status (str): Статус задачи (по умолчанию 'created')

    Response:
        - 201 Created: Задача успешно создана
        - 400 Bad Request: Невалидные данные
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateApiView(UpdateAPIView):
    """
    API endpoint для обновления существующей задачи.

    Methods:
        PUT: Полное обновление задачи
        PATCH: Частичное обновление задачи

    Path Parameters:
        - pk (UUID): UUID задачи для обновления

    Request Body:
        Любые поля задачи для обновления

    Response:
        - 200 OK: Задача успешно обновлена
        - 400 Bad Request: Невалидные данные
        - 404 Not Found: Задача не найдена
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveApiView(RetrieveAPIView):
    """
    API endpoint для получения детальной информации о задаче.

    Methods:
        GET: Получение информации о задаче

    Path Parameters:
        - pk (UUID): UUID задачи

    Response:
        - 200 OK: Данные задачи
        - 404 Not Found: Задача не найдена
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListApiView(ListAPIView):
    """
    API endpoint для получения списка всех задач с пагинацией.

    Methods:
        GET: Получение списка задач

    Query Parameters:
        - page (int): Номер страницы
        - page_size (int): Количество задач на странице (макс. 10)

    Response:
        - 200 OK: Пагинированный список задач
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination


class TaskDeleteApiView(DestroyAPIView):
    """
    API endpoint для удаления задачи.

    Methods:
        DELETE: Удаление задачи

    Path Parameters:
        - pk (UUID): UUID задачи для удаления

    Response:
        - 204 No Content: Задача успешно удалена
        - 404 Not Found: Задача не найдена
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
