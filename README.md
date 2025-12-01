# microtask\_manager

## Описание

Проект представляет собой таск трекер, архитектура которого основана на микросервисах.

## Установка и запуск

### Клонировать репозиторий

```bash
git clone git@github.com:NovoselovSV/microtask_manager.git
```

### Установить зависимости для сервисов:
```bash
cd path/to/repo/service
poetry install
```
### При необходимости активировать виртуальное окружение:
```bash
eval $(poetry env activate)
```

### Запустить проект не в контейнерах:
Проект требует работающих и настроеных приложенией PostgreSQL и RabbitMQ.
При необходимости контейнеры можно создать следующим образом:
```bash
docker run --name <Название контейнера для микросервиса users, например user_postgres> -p <Номер порта на хосте, например 5432>:5432 -e POSTGRES_PASSWORD=<Пароль для пользователя PostgreSQL для микросервиса users, по умолчанию general_user_pass> -e POSTGRES_USER=<Имя пользователя PostgreSQL для микросервиса users, по умолчанию general_user> -e POSTGRES_DB=<Имя БД PostgreSQL для микросервиса users, по умолчанию users> -d postgres
docker run --name <Название контейнера для микросервиса tasks, например task_postgres> -p <Номер порта на хосте, например 5432>:5432 -e POSTGRES_PASSWORD=<Пароль для пользователя PostgreSQL для микросервиса tasks, по умолчанию general_user_pass> -e POSTGRES_USER=<Имя пользователя PostgreSQL для микросервиса tasks, по умолчанию general_user> -e POSTGRES_DB=<Имя БД PostgreSQL для микросервиса tasks, по умолчанию tasks> -d postgres
docker run --name <Название контейнера для RabbitMQ> -p <Номер порта на хосте, по умолчанию 5672>:5672 [-p 15672:15672] -d rabbitmq:3-management
```
Значения по умолчанию можно переопределить установкой переменных окружения или в .env файле, там где есть .env.example файлы.

Если ранее не проводились миграции их надо провести на данном этапе (сервисы users и tasks).

```bash
cd path/to/repo/service/src/service
alembic upgrade head
```
Для запуска сервисов необходимо в разных процессах запустить сервисы:
users
```bash
cd path/to/repo/users-service/src/users_service
uvicorn main:app --host 0.0.0.0 --port 8000
```
tasks
```bash
cd path/to/repo/tasks-service/src/tasks_service
uvicorn main:app --host 0.0.0.0 --port 8001
```
notifications
```bash
cd path/to/repo/notifications-service/src/notifications_service
faststream run faststream_app:faststream_app
```
Сервисы будут доступны на:

users: http://localhost:8000[/docs#/]

tasks: http://localhost:8001[/docs#/]

## Примеры запросов к sse (httpie)

users sse: http --stream :8000/users/v1/sse "Authorization: Bearer <token>"

tasks sse: http --stream :8001/tasks/v1/sse "Auth: Bearer <token>"

## Использованные технологии

 1. FastAPI
 2. SQLAlchemy
 3. Alembic
 4. Faststream

## TODO
- [x] Доделать Readme
- [ ] Положить все в контейнеры и настроить docker compose
- [ ] Создать фронт
- [ ] Создать тесты

## Автор
[Новоселов Сергей](https://github.com/NovoselovSV)
