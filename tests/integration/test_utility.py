from src.authentication.auth import create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta
from jose import jwt


def test_create_access_token():
    access_token = create_access_token(data={"sub": "test_user"})
    assert access_token is not None


def test_create_access_token_with_expiration():
    access_token = create_access_token(
        data={"sub": "test_user"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    assert access_token is not None


def test_decode_token():
    access_token = create_access_token(data={"sub": "test_user"})
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "test_user"
