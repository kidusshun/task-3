from src.authentication.auth import create_access_token
from unittest.mock import MagicMock
from uuid import uuid4

from datetime import datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import Base
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dotenv import load_dotenv
import os
from config import SECRET_KEY, ALGORITHM
from jose import jwt


load_dotenv()

TEST_SQLALCHEMY_DATABASE_URL = os.getenv("TEST_SQLALCHEMY_DATABASE_URL")


def test_create_access_token(db_session):
    access_token = create_access_token(data={"sub": "test_user"})
    assert access_token is not None


def test_create_access_token_with_expiration():
    access_token = create_access_token(
        data={"sub": "test_user"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    assert access_token is not None


def test_decode_toke():
    access_token = create_access_token(data={"sub": "test_user"})
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "test_user"


def test_sign_up(client):
    response = client.post(
        "/create/",
        json={
            "username": "test_user",
            "email": "k@gmail.com",
            "password": "test_password",
            "name": "test_name",
            "bio": "test_bio",
            "role": "user",
        },
    )
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["username"] == "test_usr"
