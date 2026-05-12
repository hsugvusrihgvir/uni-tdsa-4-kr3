from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db import get_user
from security import get_payload_from_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = get_payload_from_token(token)

    username = payload.get("sub")
    role = payload.get("role")

    user = get_user(username)

    if user is None or user.role != role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    return user


def admin_auth(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return True


def user_auth(user = Depends(get_current_user)):
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return True


def guest_auth(user = Depends(get_current_user)):
    if user.role not in ["admin", "user", "guest"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return True