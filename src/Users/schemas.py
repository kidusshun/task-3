from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime


class TokenData(BaseModel):
    username: str | None = None


class UserUpdate(BaseModel):
    username: str = Field(None)
    email: str = Field(None)
    name: str = Field(None)
    password: str = Field(None)
    bio: str = Field(None)
    role: str = Field(None)
    updatedAt: datetime = Field(None)

    class Config:
        orm_mode = True
