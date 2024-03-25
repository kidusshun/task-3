from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
class TokenData(BaseModel):
    username: str | None = None


class CreateBlogRating(BaseModel):
    blogID: UUID
    rating: int = Field(..., ge=1, le=5)
    createdAt: datetime
    updatedAt: datetime

    