# 🍽️ DF2 — Сайт для бронирования столиков в ресторане

Веб-приложение для бронирования столиков в ресторане. Дипломный проект по Django + Bootstrap.

## 📋 Функционал

- **Главная** — описание ресторана, услуги, команда, контактная информация, форма обратной связи.
- **О ресторане** — история, миссия, ценности, команда.
- **Бронирование** — форма выбора столика, даты, времени, количества гостей с валидацией.
- **Личный кабинет** — регистрация, авторизация, история броней, редактирование и отмена.
- **Контакты** — форма обратной связи, контактная информация.
- **Админка** — управление пользователями, бронями, контентом (услуги, столы, команда).

## 🛠️ Стек технологий

| Технология | Назначение |
|---|---|
| **Python 3.14** | Язык программирования |
| **Django 6.1** | Веб-фреймворк |
| **PostgreSQL 16** | База данных |
| **Bootstrap 5** | Фронтенд-фреймворк |
| **Poetry** | Управление зависимостями |
| **Docker + Docker Compose** | Контейнеризация |
| **Gunicorn** | WSGI-сервер |
| **WhiteNoise** | Раздача статики в production |

## 📁 Структура проекта

```
restaurant_booking/
├── booking/                     # Приложение "Бронирование"
│   ├── fixtures/
│   │   └── initial_data.json    # Демо-данные (услуги, столы, команда)
│   ├── migrations/              # Миграции БД
│   ├── templates/booking/       # HTML-шаблоны
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── booking.html
│   │   ├── booking_success.html
│   │   ├── booking_cancel.html
│   │   ├── my_bookings.html
│   │   ├── contacts.html
│   │   ├── login.html
│   │   └── register.html
│   ├── admin.py                 # Настройка админки
│   ├── forms.py                 # Формы (Booking, Contact, Register)
│   ├── models.py                # Модели (Service, TeamMember, Table, Booking, ContactMessage)
│   ├── urls.py                  # Маршруты приложения
│   └── views.py                 # Представления
├── config/                      # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── .dockerignore                # Исключения для Docker
├── .env.example                 # Шаблон переменных окружения
├── .gitignore
├── Dockerfile                   # Образ Django
├── docker-compose.yml           # Django + PostgreSQL
├── manage.py
├── poetry.lock                  # Lock-файл зависимостей
├── pyproject.toml               # Зависимости Poetry
├── requirements.txt             # Зависимости (для Docker)
└── README.md
```

## 🚀 Установка и запуск

### Вариант 1: Docker (рекомендуется)

**Требования:** Docker Desktop.

```bash
# 1. Клонировать репозиторий
git clone https://github.com/marfuta07/restaurant_booking.git
cd restaurant_booking

# 2. Запустить контейнеры
docker compose up --build

# 3. Создать суперпользователя (в отдельном терминале)
docker compose exec web python manage.py createsuperuser

# 4. (Опционально) Загрузить демо-данные
docker compose exec web python manage.py loaddata initial_data
```

**Сайт:** http://localhost:8000
**Админка:** http://localhost:8000/admin

**Остановка:**
```bash
docker compose down
```

### Вариант 2: Локально (Poetry + SQLite)

**Требования:** Python 3.14, Poetry.

```bash
# 1. Клонировать репозиторий
git clone https://github.com/marfuta07/restaurant_booking.git
cd restaurant_booking

# 2. Установить зависимости
poetry install

# 3. Создать .env (скопировать из .env.example)
copy .env.example .env

# 4. Применить миграции
poetry run python manage.py migrate

# 5. (Опционально) Загрузить демо-данные
poetry run python manage.py loaddata initial_data

# 6. Создать суперпользователя
poetry run python manage.py createsuperuser

# 7. Запустить
poetry run python manage.py runserver
```

**Сайт:** http://127.0.0.1:8000

## 🔐 Переменные окружения

Создайте `.env` на основе `.env.example`:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (для локальной разработки — SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Для Docker — PostgreSQL (задаётся в docker-compose.yml)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=restaurant_db
# DB_USER=restaurant_user
# DB_PASSWORD=restaurant_password
# DB_HOST=db
# DB_PORT=5432
```

## 🧪 Тестирование

Проект проверен на:
- Регистрацию и авторизацию пользователей.
- Создание, редактирование и отмену броней.
- Валидацию: прошедшая дата, превышение вместимости столика, занятость столика.
- **IDOR-защиту**: пользователь не может открыть чужую бронь (404).
- Форму обратной связи.
- Загрузку фото команды через админку.

## 📊 Модели данных

| Модель | Описание |
|---|---|
| `Service` | Услуги ресторана (название, описание, иконка) |
| `TeamMember` | Члены команды (имя, роль, фото) |
| `Table` | Столики (номер, вместимость, активность) |
| `Booking` | Бронирования (пользователь, столик, дата, время, гости, статус) |
| `ContactMessage` | Сообщения обратной связи |

## 🎯 Ключевые технические решения

- **12-factor app** — конфигурация через `.env`, секреты не в коде.
- **IDOR-защита** — `get_object_or_404(Booking, pk=pk, user=request.user)`.
- **PRG-паттерн** — Post/Redirect/Get после форм (предотвращает дублирование).
- **Кастомная валидация** — в `BookingForm.clean()` (прошедшая дата, вместимость, занятость).
- **Docker** — Django + PostgreSQL, volumes для данных.
- **WhiteNoise** — раздача статики без nginx.

## 👩‍💻 Автор

**Юлия Бусыгина** — [ubusygina747@gmail.com](mailto:ubusygina747@gmail.com)

## 📄 Лицензия

Учебный проект (дипломная работа), 2026.