from datetime import datetime, UTC
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException, status, Query
from fastapi import APIRouter
from sqlalchemy.orm import Session, selectinload
from src.Blog.schemas import BlogCreate, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.models import Blog, User, Tags, get_db
from dotenv import load_dotenv
from jose import JWTError, jwt
import os
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

router = APIRouter(tags=["Blogs"])
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


@router.post("/create_blog")
async def create_blog(
    blogCreate: BlogCreate,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    new_blog = Blog(
        blogID=uuid4(),
        title=blogCreate.title,
        content=blogCreate.content,
        userID=user.id,
        createdAt=datetime.now(UTC),
        updatedAt=datetime.now(UTC),
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/get_all_blog")
async def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    if blogs:
        for blog in blogs:
            blog.blog_ratings
            blog.blog_tags
        return blogs
    raise HTTPException(status_code=404, detail="No Blogs found")


@router.get("/get_blog/{blogID}")
async def get_blog(blogID: UUID, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.blogID == blogID).first()
    if blog:
        blog.blog_ratings
        blog.blog_tags
        blog.comments
        blog.Likes
        blog.Shares
        return blog
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


@router.put("/update_blog")
async def update_blog(
    blogID: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
    title: Annotated[str | None, Query()] = None,
    content: Annotated[str | None, Query()] = None,
):
    if title and content:
        blog = (
            db.query(Blog)
            .filter(Blog.blogID == blogID)
            .update(
                {
                    Blog.title: title,
                    Blog.content: content,
                    Blog.updatedAt: datetime.now(UTC),
                }
            )
        )
    elif title:
        blog = (
            db.query(Blog)
            .filter(Blog.blogID == blogID)
            .update({Blog.title: title, Blog.updatedAt: datetime.now(UTC)})
        )
    elif content:
        blog = (
            db.query(Blog)
            .filter(Blog.blogID == blogID)
            .update({Blog.content: content, Blog.updatedAt: datetime.now(UTC)})
        )
    else:
        raise HTTPException(status_code=400, detail="No data to update")

    if blog:
        db.commit()
        return {"message": "Blog updated"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


@router.delete("/delete_blog")
async def delete_blog(
    blogID: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    blog = db.query(Blog).filter(Blog.blogID == blogID).first()
    if blog:
        if blog.userID == user.id:
            db.delete(blog)
            db.commit()
            return {"message": "Blog deleted"}
        else:
            raise HTTPException(
                status_code=401, detail="You are not authorized to delete this blog"
            )
    else:
        raise HTTPException(status_code=404, detail="Blog not found")
