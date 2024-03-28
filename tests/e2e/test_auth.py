from src.authentication.auth import create_access_token, verify_password
from unittest.mock import MagicMock
from uuid import uuid4

from datetime import datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dotenv import load_dotenv
import os
from config import SECRET_KEY, ALGORITHM
from jose import jwt


def test_sign_up(client, db_session):
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

    assert response_json["username"] == "test_user"
    assert response_json["email"] == "k@gmail.com"
    assert response_json["name"] == "test_name"
    assert response_json["bio"] == "test_bio"
    assert response_json["role"] == "user"


def test_sign_up_already_exists(client):
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
    assert response.status_code == 409


def test_login(client):
    response = client.post(
        "/login/",
        data={"username": "test_user", "password": "test_password"},
    )
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["access_token"] is not None
    assert response_json["token_type"] == "bearer"
