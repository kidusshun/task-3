def test_create_blog_rating(client, created_blog, loggedin_user):
    headers = {
        "Authorization": f"Bearer {loggedin_user}",
    }
    response = client.post(
        "/rate_blog/",
        headers=headers,
        json={
            "blogID": created_blog,
            "rating": 5,
        },
    )

    # print(response.json())
    # assert response.status_code == 200
