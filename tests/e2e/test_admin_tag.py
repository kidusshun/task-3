def test_create_tag(client, loggedin_user):
    header = {
        "Authorization": f"Bearer {loggedin_user}",
    }

    response = client.post(
        "/create_tag/",
        headers=header,
        json={
            "TagName": "sth",
        },
    )

    response.status_code == 200
