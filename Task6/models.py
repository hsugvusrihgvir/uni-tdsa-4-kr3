from pydantic import BaseModel
from pydantic_settings import BaseSettings

# ЗАДАНИЕ 6.1-6.2

class UserBase(BaseModel):
    username: str

class User(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

# ЗАДАНИЕ 6.2
class Settings(BaseSettings):
    MODE: str
    DOCS_USER: str
    DOCS_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()