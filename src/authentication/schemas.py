from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password: str
    username: str
    
    name: str
    bio: str
    role: str
    createdAt: datetime
    updatedAt: datetime

class UserLogin(UserBase):
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None