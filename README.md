# Кошачий благотворительный фонд
Сервис для поддержки котиков! Благотворительная платформа, позволяющая пользователям делать пожертвования на поддержание кошачьей преступности.


## Функциональность

- Аутентификация и авторизация пользователей (JWT)

- Разделение прав доступа (обычные пользователи и суперпользователи)

- Создание и управление благотворительными проектами (для администратора)

- Возможность делать пожертвования

- Автоматическое распределение средств между проектами

- **Формирование отчетов в Google Таблицах** (для администратора)

## Стек технологий

![FastApi](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets%20API-34A853?logo=googlesheets&logoColor=white)

## Требования

- Python 3.9+
- pip (менеджер пакетов Python)
- Аккаунт Google Cloud Platform (для работы с Google Sheets API)

## Установка

Клонируйте репозиторий:

```
git clone https://github.com/Frenky19/cat_charity_fund.git
```

Создайте файл .env в корневой директории со следующим содержимым:

```
# Настройки приложения
APP_TITLE=Название приложения
APP_DESCRIPTION=Описание приложения
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db (sqlite для разработки)
SECRET=секретный код (произвольный)
FIRST_SUPERUSER_EMAIL=e-mail для автоматического создания суперпользователя (произвольный)
FIRST_SUPERUSER_PASSWORD=пароль для автоматического создания суперпользователя (произвольный)

# Настройки Google Cloud (данные из json сервисного аккаунта)
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nМНОГО_СИМВОЛОВ\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com
EMAIL=your-personal-email@gmail.com

# ID предварительно созданной Google таблицы
SPREADSHEET_ID=your_google_sheets_id
```

Создайте виртуальное окружение и активируйте его:

```
python -m venv .venv
source .venv/bin/activate # Linux
source .venv\Scripts\activate # Windows
```

Установите зависимости:

```
pip install -r requirements.txt
```

Примените миграции:

```
alembic upgrade heads
```

Запустите приложение:

```
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

Документация API доступна по адресу: http://localhost:8000/docs

## Модели данных

### Пользователи (User)

- id - уникальный идентификатор

- email - электронная почта

- hashed_password - хешированный пароль

- is_active - статус активности

- is_superuser - является ли суперпользователем

- is_verified - подтвержден ли email

### Проекты (CharityProject)

- id - уникальный идентификатор

- name - название проекта (уникальное)

- description - описание проекта

- full_amount - требуемая сумма

- invested_amount - внесенная сумма

- fully_invested - собрана ли нужная сумма

- create_date - дата создания

- close_date - дата закрытия (если проект завершен)

### Пожертвования (Donation)

- id - уникальный идентификатор

- user_id - ID пользователя, сделавшего пожертвование

- comment - комментарий к пожертвованию

- full_amount - сумма пожертвования

- invested_amount - распределенная сумма

- fully_invested - все ли деньги распределены

- create_date - дата пожертвования

- close_date - дата полного распределения средств

## API Endpoints

### Аутентификация

- POST /auth/jwt/login - вход и получение JWT токена

- POST /auth/jwt/logout - выход

- POST /auth/register - регистрация нового пользователя

### Пользователи

- GET /users/me - информация о текущем пользователе

- PATCH /users/me - обновление информации о текущем пользователе

- GET /users/{id} - информация о пользователе (только для суперпользователей)

- PATCH /users/{id} - обновление информации о пользователе (только для суперпользователей)

### Проекты

- GET /charity_project/ - список всех проектов (доступно без авторизации)

- POST /charity_project/ - создание проекта (только для суперпользователей)

- DELETE /charity_project/{project_id} - удаление проекта (только для суперпользователей)

- PATCH /charity_project/{project_id} - обновление проекта (только для суперпользователей)

### Пожертвования

- GET /donation/ - список всех пожертвований (только для суперпользователей)

- POST /donation/ - создание пожертвования (для авторизованных пользователей)

- GET /donation/my - список пожертвований текущего пользователя

### Отчеты Google

- POST /google/ - создание/обновление отчета в Google Таблицах (только для суперпользователей)

### Процесс инвестирования

- При создании нового проекта или пожертвования автоматически запускается процесс распределения средств:

- При создании проекта система ищет незакрытые пожертвования и распределяет их средства

- При создании пожертвования система ищет незакрытые проекты и распределяет средства в них

- Когда проект или пожертвование полностью финансируются, они помечаются как закрытые

## Система отчетности

### Формирование отчетов в Google Таблицах

Система автоматически генерирует отчеты с закрытыми проектами, отсортированными по скорости сбора средств:

- **Отчет включает**: название проекта, время сбора, описание
- **Сортировка**: от самых быстрых к самым медленным проектам
- **Форматирование**: автоматическое форматирование заголовков и данных
- **Обновление**: при каждом запросе отчет полностью обновляется

### Пример отчета:

| Название проекта |   Время сбора   |  Описание  | Собрано средств |   Дата закрытия  |
|------------------|-----------------|------------|-----------------|------------------|
| Project_2        | 1 день, 0:34:59 | Описание_2 |      100000     | 2025-11-04 16:39 |
| Project_3        | 2 дня, 0:00:00  | Описание_3 |      29010      | 2025-08-22 12:07 |
| Project_1        | 4 дня, 0:04:58  | Описание_1 |      35000      | 2025-08-22 12:04 |

## Права доступа

### Обычные пользователи

- Могут регистрироваться и входить в систему

- Могут просматривать список проектов

- Могут делать пожертвования

- Могут просматривать только свои пожертвования

### Суперпользователи

- Могут выполнять все действия обычных пользователей

- Могут создавать, обновлять и удалять проекты

- Могут просматривать все пожертвования

- Могут управлять пользователями

## Структура проекта

```
app/
├── core/           # Основные настройки и конфигурация
├── models/         # Модели данных
├── schemas/        # Pydantic схемы
├── crud/           # Операции с базой данных
├── api/            # Эндпоинты API
│   └── endpoints/  # Отдельные файлы с эндпоинтами
├── services/       # Бизнес-логика (процесс инвестирования)
└── main.py         # Точка входа в приложение
```

## Автор  
[Андрей Головушкин / Andrey Golovushkin](https://github.com/Frenky19)