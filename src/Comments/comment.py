import os
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models import Blog, Comments, User, get_db

from .schemas import CreateComment, DeleteComment, TokenData, UpdateComment

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


router = APIRouter(tags=["comment"])


@router.post("/create_comment")
async def create_comment(
    payload: CreateComment,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):

    blog = db.query(Blog).filter(payload.BlogID == Blog.blogID).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    comment = Comments(
        CommentID=uuid4(),
        UserID=user.id,
        BlogID=payload.BlogID,
        content=payload.content,
        CreatedAt=payload.createdAt,
        UpdatedAt=payload.updatedAt,
    )

    db.add(comment)
    db.commit()

    db.refresh(comment)

    return comment.__dict__


@router.put("/update_comment")
async def update_comment(
    updateComment: UpdateComment,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    comment = (
        db.query(Comments).filter(Comments.CommentID == updateComment.CommentID).first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.UserID != user.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to update this comment"
        )

    comment.content = updateComment.comment
    db.commit()
    db.refresh(comment)

    return {"message": "Comment updated successfully"}


@router.delete("/delete_comment")
async def delete_comment(
    payload: DeleteComment,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    comment = db.query(Comments).filter(Comments.CommentID == payload.CommentID).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.UserID != user.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to delete this comment"
        )

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}
