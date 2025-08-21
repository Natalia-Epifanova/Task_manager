# 🚀 Менеджер задач (Task Manager)

Django REST API для управления задачами с полным CRUD функционалом и тестами.

## 🛠️ Технологический стек

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Testing**: pytest + pytest-django
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Containerization**: Docker + Docker Compose

## 📋 Функциональность

- Создание задач (CREATE)
- Просмотр списка задач (READ list) с пагинацией
- Просмотр деталей задачи (READ single)
- Обновление задач (UPDATE)
- Удаление задач (DELETE)
- Валидация данных
- Автодокументация API

## 🏗️ Модель данных

Task:
- uuid: UUID (primary key)
- title: CharField(100) - название задачи
- description: TextField(500) - описание (опционально)
- status: CharField - статус: created/underway/completed

## Быстрый старт
1. Вариант 1: Docker (рекомендуется)

```git clone https://github.com/Natalia-Epifanova/Task_manager```

```cd task_manager_django```

Запуск с Docker

```docker-compose up --build```

- Приложение будет доступно по http://localhost:8000
- API документация: http://localhost:8000/swagger/

2. Вариант 2: Локальная установка

- Создание виртуального окружения

```python -m venv venv```

```source venv/bin/activate```  # Linux/Mac

```venv\Scripts\activate```     # Windows

- Установка зависимостей

```pip install -r requirements.txt```

- Настройка базы данных

```python manage.py migrate```

- Запуск сервера

```python manage.py runserver```

- Приложение будет доступно по http://127.0.0.1:8000


## API Endpoints

```GET	/tasks/```	- Список задач с пагинацией

```POST	/tasks/create/``` -	Создание новой задачи

```GET	/tasks/{uuid}/``` -	Получение задачи по UUID

```PUT	/tasks/{uuid}/update/``` -	Обновление задачи

```DELETE	/tasks/{uuid}/delete/``` -	Удаление задачи

## Тестирование

- Запуск всех тестов

```pytest```

- Запуск с покрытием кода

```pytest --cov=tasks --cov-report=html```

Разработано: Епифанова Наталия © 2025