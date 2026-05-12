from secrets import compare_digest
from models import User

from fastapi import HTTPException, status

from models import UserInDB
from passlib.context import CryptContext

context = CryptContext(
    schemes=["bcrypt"],   # используем bcrypt
    deprecated="auto"
)


# ЗАДАНИЕ 6.1
USERS = [{"name": "name1",
          "password": "p1"},
         {"name": "name2",
          "password": "p2"}]

def get_user_from_list(username: str):
    for user in USERS:
        if user["name"] == username:
            return user

# ЗАДАНИЕ 6.2


fake_users_db = [
    UserInDB(**{
        "username": "name1",
        "hashed_password": "$2b$12$wQJDeRFf.YGI8T29j3MPjeN9euATQlqlGvbsXgiwRXuhgxD79OaTm"
    }),
    UserInDB(**{
        "username": "name2",
        "hashed_password": "$2b$12$jMRfHLmRsn4LzOQ3ynhovuxULYT6y3PVopy/rlKAHlf0Z4r.ZNGx6"
    })
]

def get_user2(username: str) -> UserInDB | None:
    for user in fake_users_db:
        if compare_digest(user.username, username):
            return user

def insert_user(username: str, password: str) -> bool:
    for user in fake_users_db:
        if compare_digest(user.username, username):
            return False
    fake_users_db.append(UserInDB(**{"username": username, "hashed_password": context.hash(password)}))
    return True

# ЗАДАНИЕ 6.4


def check_user4(user: User) -> bool:
    for db_user in fake_users_db:
        if compare_digest(db_user.username, user.username):
            if context.verify(user.password, db_user.hashed_password):
                return True
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}, detail="Authorization failed")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, headers={"WWW-Authenticate": "Bearer"}, detail="User not found")

def check_username(username: str) -> bool:
    if username is None:
        return False

    for db_user in fake_users_db:
        if compare_digest(db_user.username, username):
            return True
    return False