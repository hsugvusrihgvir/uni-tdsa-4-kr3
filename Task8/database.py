import sqlite3


DATABASE_NAME = "app.db"


def db():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ЗАДАНИЕ 8.1
def create_users_table():
    connection = db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_user(username: str, password: str):
    connection = db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    connection.commit()
    connection.close()


# ЗАДАНИЕ 8.2
def create_todos_table():
    connection = db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def insert_todo(title: str, description: str):
    connection = db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (title, description, 0)
    )

    connection.commit()
    todo_id = cursor.lastrowid
    connection.close()

    return {
        "id": todo_id,
        "title": title,
        "description": description,
        "completed": False
    }


def get_todo(todo_id: int):
    connection = db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    )

    todo = cursor.fetchone()
    connection.close()

    if todo is None:
        return None

    return {
        "id": todo["id"],
        "title": todo["title"],
        "description": todo["description"],
        "completed": bool(todo["completed"])
    }


def update_todo(todo_id: int, title: str, description: str, completed: bool):
    connection = db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    )

    todo = cursor.fetchone()

    if todo is None:
        connection.close()
        return None

    cursor.execute(
        """
        UPDATE todos
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (title, description, int(completed), todo_id)
    )

    connection.commit()
    connection.close()

    return {
        "id": todo_id,
        "title": title,
        "description": description,
        "completed": completed
    }


def delete_todo(todo_id: int) -> bool:
    connection = db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    )

    todo = cursor.fetchone()

    if todo is None:
        connection.close()
        return False

    cursor.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )

    connection.commit()
    connection.close()

    return True