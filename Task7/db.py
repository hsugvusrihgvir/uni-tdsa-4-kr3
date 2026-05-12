from fastapi import HTTPException, status
from secrets import compare_digest
from passlib.context import CryptContext
from models import User, UserInDB


context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


ROLES = ["admin", "user", "guest"]


fake_users_db = []


def get_user(username: str) -> UserInDB | None:
    for user in fake_users_db:
        if compare_digest(user.username, username):
            return user


def insert_user(user: User) -> bool:
    for db_user in fake_users_db:
        if compare_digest(db_user.username, user.username):
            return False

    if user.role not in ROLES:
        return False

    fake_users_db.append(
        UserInDB(
            username=user.username,
            hashed_password=context.hash(user.password),
            role=user.role
        )
    )

    return True


def check_user(user: User) -> UserInDB:
    for db_user in fake_users_db:
        if compare_digest(db_user.username, user.username):

            if context.verify(user.password, db_user.hashed_password):
                return db_user

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed",
                                headers={"WWW-Authenticate": "Bearer"})

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")