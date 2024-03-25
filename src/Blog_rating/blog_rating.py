import os
from typing import Annotated
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from authentication.auth import get_current_active_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models import Blog, BlogRatings, User, get_db

from .schemas import CreateBlogRating, TokenData

router = APIRouter(tags=["Blog Rating"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/rate_blog")
async def rate_blog(
    createRating: CreateBlogRating,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    blog = db.query(Blog).filter(Blog.blogID == createRating.blogID).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_rating = (
        db.query(BlogRatings)
        .filter(
            BlogRatings.blogID == createRating.blogID, BlogRatings.userID == user.id
        )
        .first()
    )
    if not blog_rating:
        new_blog_rating = BlogRatings(
            blogRatingID=uuid4(),
            blogID=createRating.blogID,
            userID=user.id,
            rating=createRating.rating,
            createdAt=createRating.createdAt,
            updatedAt=createRating.updatedAt,
        )
        db.add(new_blog_rating)
        db.commit()
        db.refresh(new_blog_rating)
        return new_blog_rating.__dict__
    else:
        blog_rating.rating = createRating.rating
        blog_rating.updatedAt = createRating.updatedAt
        db.commit()
        db.refresh(blog_rating)
        return blog_rating.__dict__
