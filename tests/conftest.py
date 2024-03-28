import pytest
from src.authentication.auth import create_access_token
from unittest.mock import MagicMock
from uuid import uuid4

from datetime import datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, engine
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from dotenv import load_dotenv
import os
from config import SECRET_KEY, ALGORITHM, TEST_SQLALCHEMY_DATABASE_URL
from jose import jwt

from fastapi.testclient import TestClient
from src.BlogTag.admin_blog_tag import get_current_active_user


from main import app


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def loggedin_user():
    token = create_access_token(data={"sub": "test_user"})
    return token


@pytest.fixture(scope="session")
def create_admin(client):
    response = client.post(
        "/create/",
        json={
            "email": "admin@gmail.com",
            "password": "pass",
            "username": "admin",
            "name": "admin",
            "bio": "hello",
            "role": "admin",
        },
    )
    response_json = response.json()
    # print(response_json)
    return response_json["username"]


@pytest.fixture(scope="session")
def loggedin_admin(create_admin):
    token = create_access_token(data={"sub": create_admin})


@pytest.fixture(scope="session")
def created_blog(client, loggedin_user):
    # Create a new blog and return its ID

    headers = {
        "Authorization": f"Bearer {loggedin_user}",
    }
    response = client.post(
        "/create_blog/",
        headers=headers,
        json={
            "title": "test_title",
            "content": "test_content",
        },
    )
    return response.json()["blogID"]


@pytest.fixture(scope="session")
def current_admin(create_admin):
    token = create_access_token(data={"sub": create_admin})
    return get_current_active_user(token)
