from src.authentication.auth import get_current_active_user
from src.BlogTag.admin_blog_tag import get_admin_role
from src.authentication.auth import create_access_token


def test_current_active_user(client, db_session):
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
    token = create_access_token(data={"sub": "test_user"})
    user = get_current_active_user(token)
    assert user is not None
