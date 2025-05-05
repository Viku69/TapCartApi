from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(...)
    mobile: str = Field(...)
    password: str = Field(...)


class UserCreate(BaseModel):
    mobile: str = Field(...)
    password: str = Field(...)
