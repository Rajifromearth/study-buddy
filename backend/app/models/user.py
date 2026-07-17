from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    password: str
    username: str = Field(min_length=2)


class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    username: str
    created_at: str