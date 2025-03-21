# QRKot

QRKot — это приложение для управления благотворительными проектами и пожертвованиями. Пользователи могут создавать проекты, вносить пожертвования, а средства автоматически распределяются между незавершёнными проектами.

## Функционал

- **Управление благотворительными проектами**:
  - Создание, обновление и удаление проектов.
  - Автоматическое распределение пожертвований на открытые проекты.
  - Возможность редактирования только определённых полей проекта.

- **Управление пожертвованиями**:
  - Пользователи могут делать пожертвования.
  - Поддержка нескольких пожертвований от одного пользователя.
  - Отдельный доступ для суперпользователей для просмотра всех пожертвований.

- **Права доступа**:
  - Обычные пользователи могут создавать пожертвования.
  - Суперпользователи имеют доступ ко всем данным.

## Инструкция по развёртыванию проекта

* Данные суперпользователя:  логин — kolya.kurenkov.1999@icloud.com пароль — kolya123
* Клонировать проект на компьютер `git clone https://github.com/foxygen-d/cat_charity_fund.git`
* Создание виртуального окружения `python3 -m venv venv`
* Запуск виртуального окружения `. venv/bin/activate`
* Установить зависимости из файла requirements.txt `pip install -r requirements.txt`
* Запуск сервера `uvicorn app.main:app`
* Запуск сервера с автоматическим рестартом `uvicorn app.main:app --reload`
* Инициализируем Alembic в проекте `alembic init --template async alembic`
* Создание файла миграции `alembic revision --autogenerate -m "migration name"`
* Применение миграций `alembic upgrade head`
* Отмена миграций `alembic downgrade`
* Запуск тестов `pytest`
   
5. **Откройте документацию: API-документация доступна по адресу http://127.0.0.1:8000/docs.**


## Структура проекта:

- app/
    - models/ — Определения таблиц базы данных.
    - crud/ — CRUD-операции для моделей.
    - schemas/ — Схемы для проверки данных.
    - api/ — Маршруты и обработчики запросов.
    - core/ — Настройки и вспомогательные функции.
- tests/ — Тесты для проверки функциональности.


## Примеры запросов

**Создание проекта (POST /charity_project/)**

```json
    {
     "name": "Котятам на НГ",
     "description": "На вкусняхи!",
     "full_amount": 100000000
    }
```

```json
    {
      "name": "Котятам на НГ",
      "description": "На вкусняхи!",
      "full_amount": 100000000,
      "id": 2,
      "invested_amount": 0,
      "fully_invested": false,
      "create_date": "2024-12-23T22:06:37.003797"
    }
```

**Создание пожертвования (POST /donation/)**

```json
    {
      "full_amount": 5000000000,
      "comment": "нака"
    }
```

```json
    {
      "full_amount": 5000000000,
      "comment": "нака",
      "id": 2,
      "create_date": "2024-12-23T22:09:16.275002"
    }
```

# Автор: 
Куренков Николай https://github.com/nugibator-hackers
