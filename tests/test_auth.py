import time

def test_register(test_client):
    unique_email = f"test_{int(time.time())}@example.com"

    response = test_client.post("/auth/register", json={
        "email": unique_email,
        "password": "test123",
        "role": "patient"
    })

    assert response.status_code in [200, 201]


def test_login(test_client):
    unique_email = f"login_{int(time.time())}@example.com"

    # register first
    test_client.post("/auth/register", json={
        "email": unique_email,
        "password": "test123",
        "role": "patient"
    })

    # login
    response = test_client.post("/auth/login", json={
        "email": unique_email,
        "password": "test123"
    })

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert "access_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"


def test_login_fail(test_client):
    response = test_client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrong123"
    })

    assert response.status_code in [400, 401, 404]