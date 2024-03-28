from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from pydantic import Field


class BlogCreate(BaseModel):
    title: str
    content: str


class UpdateBlog(BaseModel):
    title: str = Field(None)
    content: str = Field(None)


class TokenData(BaseModel):
    username: str | None = None
