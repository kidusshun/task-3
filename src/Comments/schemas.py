from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TokenData(BaseModel):
    username: str | None = None


class CreateComment(BaseModel):
    BlogID: UUID
    content: str
    createdAt: datetime
    updatedAt: datetime


class UpdateComment(BaseModel):
    CommentID: UUID
    BlogID: UUID
    comment: str

class DeleteComment(BaseModel):
    CommentID: UUID