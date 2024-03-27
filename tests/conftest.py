import pytest
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
from config import SECRET_KEY, ALGORITHM, TEST_SQLALCHEMY_DATABASE_URL
from jose import jwt

from fastapi.testclient import TestClient


from main import app


@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client
