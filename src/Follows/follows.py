from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from models import User, Comments, Blog, Follows, get_db
from .schemas import TokenData, FollowUser, UnFollowUser
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
from datetime import datetime, UTC

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


router = APIRouter(tags=["follow"])


@router.post("/follow")
async def follow(
    payload: FollowUser,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if user.id == payload.FollowedID:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    if db.query(User).filter(User.id == payload.FollowedID).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    if (
        db.query(Follows)
        .filter(Follows.FollowerID == user.id, Follows.FollowedID == payload.FollowedID)
        .first()
        is not None
    ):
        raise HTTPException(
            status_code=400, detail="You are already following this user"
        )

    db_follow = Follows(
        FollowID=uuid4(),
        FollowerID=user.id,
        FollowedID=payload.FollowedID,
        CreatedAt=datetime.now(UTC),
        UpdatedAt=datetime.now(UTC),
    )
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


@router.delete("/unfollow")
async def unfollow(
    payload: UnFollowUser,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_follow = (
        db.query(Follows)
        .filter(payload.FollowedID == Follows.FollowedID, Follows.FollowerID == user.id)
        .first()
    )

    if not db_follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    db.delete(db_follow)
    db.commit()

    return {"detail": "User unfollowed"}
