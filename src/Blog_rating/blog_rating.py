from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.authentication.auth import get_current_active_user
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
            createdAt=datetime.now(UTC),
            updatedAt=datetime.now(UTC),
        )
        db.add(new_blog_rating)
        db.commit()
        db.refresh(new_blog_rating)
        return new_blog_rating.__dict__
    else:
        raise HTTPException(status_code=400, detail="Rating already exists")


@router.put("/update_rating")
async def update_blog_raing(
    updateRating: CreateBlogRating,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    blog_rating = (
        db.query(BlogRatings)
        .filter(
            BlogRatings.blogID == updateRating.blogID, BlogRatings.userID == user.id
        )
        .first()
    )

    if not blog_rating:
        raise HTTPException(status_code=404, detail="blog rating not found")
    blog_rating.rating = updateRating.rating
    blog_rating.updatedAt = datetime.now(UTC)
    db.commit()
    db.refresh(blog_rating)
    return {"message": "Rating updated successfully"}
