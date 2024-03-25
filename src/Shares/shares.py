import os
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from models import Blog, Shares, User, get_db

from .schemas import ShareBlog, TokenData

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


router = APIRouter(tags=["shares"])


@router.post("/share")
async def share_blog(
    payload: ShareBlog,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    blog = db.query(Blog).filter(payload.BlogID == Blog.blogID).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    share = Shares(
        ShareID=uuid4(),
        UserID=user.id,
        BlogID=payload.BlogID,
        CreatedAt=payload.CreatedAt,
        UpdatedAt=payload.UpdatedAt,
    )

    db.add(share)
    db.commit()
    db.refresh(share)

    return share.__dict__
