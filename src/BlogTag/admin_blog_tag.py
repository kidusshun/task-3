import os
from datetime import UTC, datetime
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from models import Tags, User, get_db

from .schemas import Tag, TokenData, UpdateTag

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


async def get_admin_role(user: User = Depends(get_current_active_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    return user


router = APIRouter(tags=["Tags"])


@router.post("/create_tag")
async def create_tag(
    create_tag: Tag,
    user: User = Depends(get_admin_role),
    db: Session = Depends(get_db),
):

    tag = db.query(Tags).filter(Tags.TagName == create_tag.TagName).first()

    if tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    tag = Tags(
        TagName=create_tag.TagName,
        createdAt=datetime.now(UTC),
        updatedAt=datetime.now(UTC),
    )

    db.add(tag)
    db.commit()

    return {"tagName": tag.TagName}


@router.get("/get_tags")
async def get_tags(db: Session = Depends(get_db)):
    return db.query(Tags).all()


@router.get("/get_tag/{tagName}")
async def get_tag_by_ID(tagName: str, db: Session = Depends(get_db)):
    tag = db.query(Tags).filter(Tags.TagName == tagName).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/update_tag")
async def update_tag(
    tag: UpdateTag,
    user: User = Depends(get_admin_role),
    db: Session = Depends(get_db),
):

    tag_db = db.query(Tags).filter(Tags.TagName == tag.OriginalTagName).first()

    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag_db.TagName = tag.UpdatedTagName
    db.commit()
    return {"message": "Tag updated successfully"}


@router.delete("/delete_tag")
def delete_tag(
    tagName: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):

    tag = db.query(Tags).filter(Tags.TagName == tagName).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
