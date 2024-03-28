def test_create_blog_rating(client, loggedin_user):
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
    blogID = response.json()["blogID"]

    response = client.post(
        "/rate_blog",
        headers=headers,
        json={"blogID": blogID, "rating": 3},
    )
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["blogID"] == blogID
    assert response_json["rating"] == 3
    assert response_json["blogRatingID"] is not None
