from uuid import uuid4


def test_create_blog(client, loggedin_user):
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
    assert response.status_code == 200
    response = response.json()
    assert response["title"] == "test_title"
    assert response["content"] == "test_content"


def test_get_all_blog(client):

    response = client.get(
        "/get_all_blog/",
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1


def test_get_blog_by_id(client, created_blog):
    response = client.get(
        f"/get_blog/{created_blog}",
    )

    assert response.status_code == 200
    response = response.json()
    assert response["title"] == "test_title"
    assert response["content"] == "test_content"


def test_update_blog(client, created_blog, loggedin_user):
    response = client.put(
        f"/update_blog/{created_blog}",
        headers={"Authorization": f"Bearer {loggedin_user}"},
        json={
            "title": "updated_title",
            "content": "updated_content",
        },
    )
    assert response.status_code == 200
    response = response.json()
    assert response["message"] == "Blog updated"


def test_update_non_existing_blog(client, loggedin_user):
    response = client.put(
        f"/update_blog/{uuid4()}",
        headers={"Authorization": f"Bearer {loggedin_user}"},
        json={
            "title": "updated_title",
            "content": "updated_content",
        },
    )
    assert response.status_code == 404
    response = response.json()
    assert response["detail"] == "Blog not found"


def test_delete_blog(client, created_blog, loggedin_user):
    response = client.delete(
        f"/delete_blog/{created_blog}",
        headers={"Authorization": f"Bearer {loggedin_user}"},
    )
    assert response.status_code == 200


def test_delete_non_existing_blog(client, loggedin_user):
    response = client.delete(
        f"/delete_blog/{uuid4()}",
        headers={"Authorization": f"Bearer {loggedin_user}"},
    )
    assert response.status_code == 404
