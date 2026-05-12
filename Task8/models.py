from pydantic import BaseModel


# ЗАДАНИЕ 8.1
class User(BaseModel):
    username: str
    password: str


# ЗАДАНИЕ 8.2
class Todo(BaseModel):
    title: str
    description: str


class TodoUpdate(Todo):
    completed: bool