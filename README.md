# cat-charity-2

QRKot — это веб-приложение на FastAPI для управления целевыми проектами и пожертвованиями в благотворительном фонде. Система автоматически распределяет поступившие пожертвования между открытыми проектами, инвестируя средства в порядке очереди (сначала самые старые проекты). Если пожертвование превышает потребность текущего проекта, остаток направляется в следующий открытый проект. Если проектов нет, нераспределённые средства ожидают появления нового проекта.

## Основные возможности
Целевые проекты – создание проектов с указанием названия, описания и требуемой суммы.

Пожертвования – приём пожертвований с комментариями (опционально).

Автоматическое инвестирование – при создании проекта или нового пожертвования средства автоматически распределяются:

Сначала заполняется самый старый открытый проект.

Если пожертвование превышает потребность проекта, остаток идёт в следующий проект.

Если проектов нет, нераспределённые средства остаются в фонде до появления нового проекта.

Полный CRUD для проектов и просмотр всех пожертвований.

Валидация – уникальность названия проекта, ограничения на длину, запрет уменьшения требуемой суммы ниже уже внесённой и т.д.

## Установка и запуск

### Клонирование репозитория

1. Клонируйте репозиторий:

```
git clone https://github.com/PugachevAndrey/cat-charity-2
```

```
cd cat-charity-2
```

2. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
```

```
source venv/bin/activate   # для Linux/Mac
source venv\Scripts\activate      # для Windows
```

3. Установите зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Настройка базы данных
Создайте файл .env в корне проекта со следующей переменной (если хотите использовать другую БД – измените URL):
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=ваш_секретный_ключ_для_JWT
```

5. Применение миграций
```
alembic upgrade head
```
Если миграций ещё нет – выполните инициализацию:
```
alembic revision --autogenerate -m "init"
alembic upgrade head
```

6. Запуск приложения
```
uvicorn app.main:app --reload
```
После запуска документация Swagger будет доступна по адресу:
```
http://127.0.0.1:8000/docs
```

## Примеры

Регистрация пользователя
```
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

```
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

Получение JWT-токена (логин)
```
curl -X POST "http://127.0.0.1:8000/auth/jwt/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Создание целевого проекта (только для суперпользователя)
```
curl -X POST "http://127.0.0.1:8000/charity_project/" \
  -H "Authorization: Bearer <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Помощь бездомным котам",
    "description": "Сбор средств на стерилизацию и корм для 100 котиков",
    "full_amount": 100000
  }'
```

```
{
  "id": 1,
  "name": "Помощь бездомным котам",
  "description": "Сбор средств на стерилизацию и корм для 100 котиков",
  "full_amount": 100000,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2025-04-10T12:00:00",
  "close_date": null
}
```

## Автор проекта
Разработчик: **Пугачев Андрей (https://github.com/PugachevAndrey)**

## Технологический стек

| Технология | Назначение | Документация |
|------------|------------|--------------|
| Python 3.12 | Язык программирования | [python.org](https://www.python.org/) |
| FastAPI | Веб-фреймворк для API | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| SQLAlchemy 2.0 | ORM для работы с базой данных | [docs.sqlalchemy.org](https://docs.sqlalchemy.org/) |
| Alembic | Управление миграциями БД | [alembic.sqlalchemy.org](https://alembic.sqlalchemy.org/) |
| Pydantic | Валидация данных и сериализация | [docs.pydantic.dev](https://docs.pydantic.dev/) |
| Uvicorn | ASGI-сервер для запуска FastAPI | [uvicorn.org](https://www.uvicorn.org/) |
| SQLite (aiosqlite) | Лёгкая реляционная БД (по умолчанию) | [sqlite.org](https://www.sqlite.org/) |
| passlib | Хеширование паролей | [passlib.readthedocs.io](https://passlib.readthedocs.io/) |