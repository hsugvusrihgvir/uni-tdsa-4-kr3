from fastapi import FastAPI, HTTPException, status
from models import User, Todo, TodoUpdate
from database import insert_user, insert_todo, get_todo, update_todo, delete_todo

app = FastAPI()

# ЗАДАНИЕ 8.1
@app.post("/register")
async def register(user: User):
    insert_user(user.username, user.password)

    return {"message": "User registered successfully!"}


# ЗАДАНИЕ 8.2
@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo):
    return insert_todo(todo.title, todo.description)


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    todo = get_todo(todo_id)

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@app.put("/todos/{todo_id}")
async def update_todo_by_id(todo_id: int, todo: TodoUpdate):
    updated_todo = update_todo(
        todo_id,
        todo.title,
        todo.description,
        todo.completed
    )

    if updated_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return updated_todo


@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int):
    if delete_todo(todo_id):
        return {"message": "Todo deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )