from pydantic import BaseModel
from uuid import UUID
from datetime import datetime



class TokenData(BaseModel):
    username: str | None = None

class FollowUser(BaseModel):
    FollowedID: UUID
    CreatedAt: datetime
    UpdatedAt: datetime

class UnFollowUser(BaseModel):
    FollowedID:UUID
