from datetime import UTC, datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from model.models import User, Comments, Blog, Likes, get_db
from .schemas import TokenData, createLike, DeleteLike
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt, JWTError
import os

from uuid import UUID, uuid4


from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


router = APIRouter(tags=["Likes"])


@router.post("/like")
async def like_blog(
    payload: createLike,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    blog = db.query(Blog).filter(payload.BlogID == Blog.blogID).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    like = Likes(
        LikeID=uuid4(),
        UserID=user.id,
        BlogID=payload.BlogID,
        CreatedAt=datetime.now(UTC),
        UpdatedAt=datetime.now(UTC),
    )

    db.add(like)
    db.commit()
    db.refresh(like)

    return like.__dict__


@router.delete("/unlike")
async def unlike_blog(
    payload: DeleteLike,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    like = (
        db.query(Likes)
        .filter(payload.BlogID == Likes.BlogID, user.id == Likes.UserID)
        .first()
    )
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()

    return {"message": "Like deleted successfully"}
