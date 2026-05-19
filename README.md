# API организационной структуры

REST API для управления организационной структурой компании: подразделениями, сотрудниками и иерархией.

## Возможности

- **Древовидная структура подразделений** с вложенностью любой глубины
- **Управление сотрудниками**: привязка к подразделениям, поиск, фильтрация
- **Перемещение подразделений** с автоматической проверкой на циклы
- **Гибкое удаление**: каскадное (`cascade`) или с переводом сотрудников (`reassign`)
- **Auto-generated Swagger документация** через `drf-yasg`
- **Полная контейнеризация** через Docker + Docker Compose
- **Покрытие тестами** (pytest) всех критических сценариев

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/SanSanForFun/organization_structure_api.git
cd organization_structure_api
```

### 2. Запустите через Docker Compose

```bash
# Сборка и запуск всех сервисов
docker-compose up --build
```

### 3. Проверьте работу

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/

### 4. Остановка

```bash
docker-compose down
```

---

## API Endpoints

### Подразделения (Departments)

| Метод    | Эндпоинт                                                                 | Описание                                 |
|----------|--------------------------------------------------------------------------|------------------------------------------|
| `POST`   | `/api/departments/create`                                                | Создать подразделение                    |
| `GET`    | `/api/departments/<id>/`                                                 | Получить детали + сотрудники + поддерево |
| `PATCH`  | `/api/departments/<id>/update`                                           | Обновить или переместить                 |
| `DELETE` | `/api/departments/<id>/delete?mode=cascade`                              | Удалить каскадно                         |
| `DELETE` | `/api/departments/<id>/delete?mode=reassign&reassign_to_department_id=5` | Удалить с переводом сотрудников          |

### Сотрудники (Employees)

| Метод  | Эндпоинт                                | Описание                           | Пример тела                                       |
|--------|-----------------------------------------|------------------------------------|---------------------------------------------------|
| `POST` | `/api/departments/<dept_id>/employees/` | Создать сотрудника в подразделении | `{"full_name": "Иванов И.И.", "position": "Dev"}` |

---

## Тестирование

### Запуск тестов в контейнере

```bash
# Все тесты
docker-compose exec web pytest -v

# С покрытием кода
docker-compose exec web pytest --cov=organization -v
```

### Локальный запуск (без Docker)

```bash
# Создайте виртуальное окружение
python -m venv .venv
source .venv/Scripts/activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Настройте переменные окружения
export DB_HOST=localhost
export DB_PASSWORD=secret
# ... остальные переменные

# Запустите тесты
pytest -v
```

---

### Технологический стек

| Компонент           | Технология                                     |
|---------------------|------------------------------------------------|
| **Фреймворк**       | Django 4.2+ / DRF 3.14+                        |
| **База данных**     | PostgreSQL 15                                  |
| **Документация**    | drf-yasg (Swagger/OpenAPI)                     |
| **Тестирование**    | pytest + pytest-django                         |
| **Контейнеризация** | Docker + Docker Compose                        |
| **Сервер**          | Gunicorn (production) / Django runserver (dev) |
| **Язык**            | Python 3.12+                                   |
