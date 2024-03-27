from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    content: str


class TokenData(BaseModel):
    username: str | None = None
