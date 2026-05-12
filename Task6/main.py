from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html

from depends import authenticate_user, auth_user, env_auth, jwt_auth
from models import User, UserInDB
from models import settings
from db import insert_user, check_user4, check_username

from security import create_jwt_token

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

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
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@app.get("/login2")
async def login2(user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}

# Задание 6.3

if settings.MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def docs(_: bool = Depends(env_auth)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="API docs"
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_json(_: bool = Depends(env_auth)):
        return app.openapi()

elif settings.MODE == "PROD":
    pass
else:
    raise ValueError("Invalid MODE. Expected DEV or PROD")

# Задание 6.4-6.5

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )

@app.post("/login5")
@limiter.limit("5/minute")
async def login5(request: Request, user: User):
    check_user4(user)
    token = create_jwt_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected_resource")
async def protected_resource(_=Depends(jwt_auth)):
    return {"message": "Access granted"}

# ЗАДАНИЕ 6.5
@app.post("/register5", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register5(request: Request, user: User):
    if insert_user(user.username, user.password):
        return {"message": "New user created"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
