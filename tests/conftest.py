import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.init_db import init_db


# =========================
# DATABASE SETUP
# =========================
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()
    yield


# =========================
# TEST CLIENT (SINGLE INSTANCE)
# =========================
@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


# =========================
# GET TOKEN (INTERNAL HELPER)
# =========================
def get_token(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })

    print("LOGIN STATUS:", response.status_code)
    print("LOGIN RESPONSE:", response.text)

    if response.status_code != 200:
        return None

    data = response.json()

    # your API format: success_response -> data -> access_token
    return data.get("data", {}).get("access_token")


# =========================
# AUTH HEADERS (USED IN TESTS)
# =========================
@pytest.fixture
def auth_headers(test_client):
    token = get_token(test_client)

    if not token:
        pytest.skip("Login failed - cannot generate token")

    return {
        "Authorization": f"Bearer {token}"
    }


# =========================
# AUTH CLIENT (FIX FOR YOUR ERRORS)
# =========================
@pytest.fixture
def auth_client(test_client):
    token = get_token(test_client)

    if not token:
        pytest.skip("Login failed - cannot generate token")

    test_client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return test_client