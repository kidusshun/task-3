from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TokenData(BaseModel):
    username: str | None = None

class ShareBlog(BaseModel):
    BlogID: UUID
    CreatedAt: datetime
    UpdatedAt: datetime
    

