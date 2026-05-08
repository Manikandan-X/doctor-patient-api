def test_root(test_client):
    response = test_client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert data["message"] == "API Running"