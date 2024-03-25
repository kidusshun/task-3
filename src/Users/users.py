import os
from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session, selectinload

from models import Blog, Tags, User, get_db

from .schemas import TokenData, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def get_current_active_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


def get_password_hash(password):
    return pwd_context.hash(password)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/update/")
async def update_user(
    updatedUser: UserUpdate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user.id).first()
    attributes = ["username", "email", "name", "password", "bio"]
    for attr in attributes:
        if getattr(updatedUser, attr) is not None:
            if attr == "password":
                setattr(user, attr, get_password_hash(getattr(updatedUser, attr)))
            else:
                setattr(user, attr, getattr(updatedUser, attr))

    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}")
async def read_users(
    user_id: UUID,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    return user


@router.delete("/delete")
async def delete_user(
    user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user.id).first()
    print(user)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
