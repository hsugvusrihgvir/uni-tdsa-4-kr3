from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html

from depends import authenticate_user, auth_user, env_auth
from models import User, UserInDB
from models import settings
from db import insert_user

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


# ЗАДАНИЕ 6.1
@app.get("/login1")
async def login1(message:str = Depends(authenticate_user)):
    return {"message": message}

# Задание 6.2

@app.post("/register2")
async def register2(user: User):
    if insert_user(user.username, user.password):
        return { "message": "User registered successfully" }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Basic"})


@app.get("/login2")
async def login2(user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}

# Задание 6.3

if settings.MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def docs(user: User = Depends(env_auth)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="API docs"
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_json(user: User = Depends(env_auth)):
        return app.openapi()

elif settings.MODE == "PROD":
    pass
else:
    raise ValueError("Invalid MODE. Expected DEV or PROD")