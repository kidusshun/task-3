from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TokenData(BaseModel):
    username: str | None = None


class Tag(BaseModel):
    TagName: str
    createdAt: datetime
    updatedAt: datetime

class UpdateTag(BaseModel):
    OriginalTagName: str
    UpdatedTagName: str

class AddTag(BaseModel):
    TagName: str
    BlogID: UUID
    createdAt: datetime
    updatedAt: datetime

class RemoveTag(BaseModel):
    BlogTagID: UUID