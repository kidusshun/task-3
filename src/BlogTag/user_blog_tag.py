from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from models import User, Tags, Blog, BlogTags, get_db
from .schemas import TokenData, Tag, AddTag, RemoveTag
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt, JWTError
import os

from uuid import UUID, uuid4

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


router = APIRouter(tags=["blog_tags"])


@router.post("/assign_tag")
async def add_tag(
    payload: AddTag,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    blog = db.query(Blog).filter(Blog.blogID == payload.BlogID).first()
    tag = db.query(Tags).filter(payload.TagName == Tags.TagName).first()
    blogTag = (
        db.query(BlogTags)
        .filter(payload.BlogID == BlogTags.BlogID, payload.TagName == BlogTags.TagName)
        .first()
    )
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.userID != user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to add tags to this blog"
        )

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if blogTag:
        raise HTTPException(status_code=409, detail="Tag already assigned to blog")

    db.add(
        BlogTags(
            BlogTagID=uuid4(),
            BlogID=payload.BlogID,
            UserID=user.id,
            TagName=payload.TagName,
            createdAt=payload.createdAt,
            updatedAt=payload.updatedAt,
        )
    )
    db.commit()
    return payload.dict()


@router.delete("/delete_blog_tag")
async def remove_tag(
    payload: RemoveTag,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    blogTag = (
        db.query(BlogTags)
        .filter(payload.BlogTagID == BlogTags.BlogTagID)
        .filter()
        .first()
    )

    if not blogTag:
        raise HTTPException(status_code=404, detail="Blog tag not found")

    if blogTag.UserID != user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to add tags to this blog"
        )

    db.delete(blogTag)
    db.commit()

    return {"message": "Tag removed successfully"}
