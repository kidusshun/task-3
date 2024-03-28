import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

TEST_SQLALCHEMY_DATABASE_URL = os.getenv("TEST_SQLALCHEMY_DATABASE_URL")
DEV_SQLALCHEMY_DATABASE_URL = os.getenv("DEV_SQLALCHEMY_DATABASE_URL")

ENVIRONMENT = os.getenv("ENVIRONMENT")


def set_database_url(environment):
    if environment == "development":
        return DEV_SQLALCHEMY_DATABASE_URL
    elif environment == "testing":
        return TEST_SQLALCHEMY_DATABASE_URL
    else:
        raise ValueError(f"Invalid environment: {environment}")


SEQLALCHEMY_DATABASE_URL = set_database_url(ENVIRONMENT)
