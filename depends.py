from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db import get_user_from_list, get_user2

from models import User, UserInDB, settings

from passlib.context import CryptContext
from secrets import compare_digest

security = HTTPBasic()

context = CryptContext(
    schemes=["bcrypt"],   # используем bcrypt
    deprecated="auto"
)

# ЗАДАНИЕ 6.1
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user = get_user_from_list(username=credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return "You got my secret, welcome"

# ЗАДАНИЕ 6.2
def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    password = credentials.password
    user = get_user2(username=credentials.username)
    if user is None or not(context.verify(password, user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user


# ЗАДАНИЕ 6.2
def env_auth(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    username, password = credentials.username, credentials.password
    if not (compare_digest(username, settings.DOCS_USER) and compare_digest(password, settings.DOCS_PASSWORD)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"})
    return True