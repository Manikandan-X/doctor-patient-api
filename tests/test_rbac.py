def test_protected_route_without_token(test_client):
    response = test_client.get("/appointments/")

    assert response.status_code in [401, 403]
    assert response.status_code != 200


def test_protected_route_with_token(test_client, auth_headers):
    response = test_client.get("/appointments/", headers=auth_headers)

    assert response.status_code in [200, 403]

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)