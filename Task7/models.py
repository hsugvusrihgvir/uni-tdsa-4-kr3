from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str
    role: str


class UserInDB(UserBase):
    hashed_password: str
    role: str


class Resource(BaseModel):
    title: str
    text: str