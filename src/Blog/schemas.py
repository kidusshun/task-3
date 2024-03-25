from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

class BlogCreate(BaseModel):
    title:str
    content:str
    createdAt: datetime
    updatedAt: datetime

class TokenData(BaseModel):
    username: str | None = None