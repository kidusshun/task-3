from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status

# from .schemas import CreateBlogRating, TokenData
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Blog, User, BlogTags, get_db
from uuid import UUID, uuid4


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/userName/{userName}")
async def get_user_by_userName(userName: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == userName).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/name/{name}")
async def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).all()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/blogTitle/{title}")
async def get_blog_by_title(title: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.title == title).all()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.get("/blogTag/{tag}")
async def get_blog_by_tag(tag: str, db: Session = Depends(get_db)):
    blogTags = db.query(BlogTags).filter(BlogTags.TagName == tag).all()
    if not blogTags:
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs = []
    for row in blogTags:
        blog = db.query(Blog).filter(Blog.blogID == row.BlogID).first()
        blogs.append(blog)
    return blogs


@router.get("/get_user/{searchTerm}")
async def get_user(searchTerm: str, db: Session = Depends(get_db)):
    users = (
        db.query(User)
        .filter(
            User.username.like(f"%{searchTerm}%"), User.name.like(f"%{searchTerm}%")
        )
        .all()
    )
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.get("/get_blog/{searchTerm}")
async def get_blog(searchTerm: str, db: Session = Depends(get_db)):
    blogs = (
        db.query(Blog)
        .filter(
            Blog.title.like(f"%{searchTerm}%"), Blog.content.like(f"%{searchTerm}%")
        )
        .all()
    )
    if not blogs:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blogs
