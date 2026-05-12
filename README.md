# Контрольная работа 3
Технологии разработки серверных приложений

* [Пример переменных окружения](Task6/.env.example)

## Тесты со скриншотами!!!!!
* [Тесты для задания 6](Task6/tests.md) !!!
* [Тесты для задания 7](Task6/tests.md) !!!
* [Тесты для задания 8](Task6/tests.md) !!!


## Установка

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Создать файл `.env` на основе `.env.example`.


## Создание таблиц для задания 8

Перед запуском задания 8 нужно один раз создать таблицы:

```bash
python create_tables.py
```

После этого появится файл базы данных:

```text
app.db
```

## Запуск приложения
Перейти в папку задания, там:
```bash
uvicorn main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```


## Задание 6


```text
GET /login1
```

```text
POST /register2
GET /login2
```

```text
POST /register5
POST /login5
GET /protected_resource
```

Документация в DEV-режиме:

```text
GET /docs
GET /openapi.json
```

## Задание 7

RBAC, доступ на основе ролей:

```text
POST /register
POST /login
GET /protected_resource
POST /resources
GET /resources
PUT /resources/{resource_id}
DELETE /resources/{resource_id}
```

Роли:

```text
admin
user
guest
```

## Задание 8

Регистрация пользователя в SQLite:

```text
POST /register
```

для Todo:

```text
POST /todos
GET /todos/{todo_id}
PUT /todos/{todo_id}
DELETE /todos/{todo_id}
```
